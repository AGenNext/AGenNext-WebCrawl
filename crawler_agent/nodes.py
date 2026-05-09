"""LangGraph nodes for the crawling workflow"""
from typing import Optional
from urllib.parse import urljoin, urlparse
import asyncio

from crawler_agent.state import CrawlState, CrawledPage
from crawler_agent.crawlers.firecrawl import FirecrawlCrawler
from crawler_agent.crawlers.crawl4ai import Crawl4AICrawler
from crawler_agent.config import (
    DEFAULT_DEPTH, DEFAULT_MAX_PAGES, DEFAULT_MAX_URLS,
    CrawlMode, CrawlProvider
)


# Global crawler instances
_firecrawl_crawler: Optional[FirecrawlCrawler] = None
_crawl4ai_crawler: Optional[Crawl4AICrawler] = None


def get_crawler(provider: str) -> "FirecrawlCrawler | Crawl4AICrawler":
    """Get or create crawler instance"""
    global _firecrawl_crawler, _crawl4ai_crawler
    
    # Normalize provider name
    if provider in ("firecrawl", "firecrawl-opensource"):
        if _firecrawl_crawler is None:
            _firecrawl_crawler = FirecrawlCrawler()
        return _firecrawl_crawler
    else:
        if _crawl4ai_crawler is None:
            _crawl4ai_crawler = Crawl4AICrawler()
        return _crawl4ai_crawler


async def crawl_single_page(state: CrawlState) -> dict:
    """Node: Crawl a single page from pending URLs"""
    
    from crawler_agent.nodes import get_crawler
    
    url = state.get("url", "")
    provider = state.get("provider", "crawl4ai")
    
    if not url:
        return {"error": "No URL provided", "status": "error"}
    
    crawler = get_crawler(provider)
    
    try:
        result = await crawler.crawl(url)
        
        page_data: CrawledPage = {
            "url": url,
            "markdown": result.get("markdown", ""),
            "html": result.get("html"),
            "links": result.get("links", []),
            "metadata": result.get("metadata", {}),
        }
        
        return {
            "crawled_pages": [page_data],
            "visited_urls": [url],
            "extracted_links": result.get("links", []),
            "total_pages": 1,
        }
        
    except Exception as e:
        return {
            "error": f"Failed to crawl {url}: {str(e)}",
            "status": "error",
        }


# Keep the old function for backward compatibility
async def crawl_page(state: CrawlState) -> dict:
    """Node: Crawl a single page (for mode-based iteration)"""
    
    # This is now handled in graph.py
    return await crawl_single_page(state)


def should_continue_crawl(state: CrawlState) -> str:
    """Edge: Decide whether to continue crawling"""
    
    mode = state.get("mode", "single")
    pending = state.get("pending_urls", [])
    visited = state.get("visited_urls", [])
    current_depth = state.get("current_depth", 0)
    depth = state.get("depth", DEFAULT_DEPTH)
    max_pages = state.get("max_pages", DEFAULT_MAX_PAGES)
    max_urls = state.get("max_urls", DEFAULT_MAX_URLS)
    
    # Handle single mode - only crawl one page
    if mode == "single":
        return "END"
    
    # Check if we hit limits
    if max_pages and state.get("total_pages", 0) >= max_pages:
        return "END"
    
    if max_urls and len(visited) >= max_urls:
        return "END"
    
    # For depth mode - stop at max depth
    if mode == "depth" and current_depth >= depth:
        return "END"
    
    # No pending URLs - nothing more to crawl
    if not pending:
        return "END"
    
    # Continue crawling
    return "CONTINUE"


def process_pending_urls(state: CrawlState) -> dict:
    """Node: Add pending URLs based on crawl mode"""
    
    mode = state.get("mode", "single")
    extracted_links = state.get("extracted_links", [])
    pending = list(state.get("pending_urls", []))
    visited = list(state.get("visited_urls", []))
    
    if mode in ["depth", "deep", "knowledge"]:
        # Add new links to pending queue (limit to prevent infinite)
        new_links = [l for l in extracted_links if l not in visited]
        
        if mode == "depth":
            # BFS - add all new links at once
            pending.extend(new_links[:10])  # Limit concurrent
        elif mode == "deep":
            # Deep crawl - add ALL new links
            max_urls = state.get("max_urls", DEFAULT_MAX_URLS)
            remaining = max_urls - len(visited) if max_urls else 999999
            pending.extend(new_links[:remaining])
        elif mode == "knowledge":
            # Knowledge mode - extract only relevant links
            relevant = _filter_relevant_links(new_links)
            pending.extend(relevant[:5])
    
    return {"pending_urls": pending}


def _filter_relevant_links(links: list) -> list:
    """Filter links that are likely to contain content (not nav, login, etc.)"""
    
    excluded_patterns = [
        "login", "signin", "register", "signup",
        "logout", "signout",
        "contact", "about", "privacy", "terms",
        "facebook", "twitter", "linkedin", "instagram",
        ".pdf", ".doc", ".docx", ".zip",
    ]
    
    filtered = []
    for link in links:
        link_lower = link.lower()
        if not any(pattern in link_lower for pattern in excluded_patterns):
            filtered.append(link)
    
    return filtered[:20]


async def extract_knowledge(state: CrawlState) -> dict:
    """Node: Extract knowledge graph from crawled content"""
    
    crawled_pages = state.get("crawled_pages", [])
    
    # Simple entity extraction from markdown
    entities = []
    relationships = []
    
    for page in crawled_pages:
        url = page.get("url", "")
        markdown = page.get("markdown", "")
        
        # Extract headings as potential entities
        lines = markdown.split("\n")
        for line in lines:
            if line.startswith("# "):
                entities.append({
                    "type": "heading",
                    "value": line[2:].strip(),
                    "source": url,
                })
            elif line.startswith("## "):
                entities.append({
                    "type": "section",
                    "value": line[3:].strip(),
                    "source": url,
                })
    
    # Build simple relationships
    for i, entity in enumerate(entities):
        if i > 0 and entities[i-1]["type"] == "heading":
            relationships.append({
                "from": entities[i-1]["value"],
                "to": entity["value"],
                "type": "contains",
            })
    
    return {
        "knowledge_graph": {
            "entities": entities,
            "relationships": relationships,
        }
    }


def end_node(state: CrawlState) -> dict:
    """Node: Finalize and return results"""
    
    return {
        "status": "completed",
    }


def error_node(state: CrawlState) -> dict:
    """Node: Handle errors"""
    
    error = state.get("error", "Unknown error")
    return {
        "status": "error",
        "error": error,
    }