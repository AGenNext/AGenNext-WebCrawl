"""LangGraph state graph definition for Web Crawling Agent (Simplified)"""
from langgraph.graph import StateGraph, END
from crawler_agent.state import CrawlState, get_initial_state
from crawler_agent.nodes import (
    crawl_single_page,
    extract_knowledge,
    end_node,
)


def create_crawl_graph():
    """Create a simple crawling state graph (single node)"""
    
    graph = StateGraph(CrawlState)
    
    # Single node that crawls one page
    graph.add_node("crawl", crawl_single_page)
    graph.add_node("extract_knowledge", extract_knowledge)
    graph.add_node("end", end_node)
    
    # Simple flow: crawl -> extract knowledge if needed -> end
    graph.set_entry_point("crawl")
    graph.add_edge("crawl", "extract_knowledge")
    graph.add_edge("extract_knowledge", "end")
    graph.add_edge("end", END)
    
    return graph


async def run_crawl(
    url: str,
    mode: str = "single",
    depth: int = 2,
    max_pages: int = 50,
    max_urls: int = 100,
    provider: str = "crawl4ai",
):
    """Run a crawl using the state graph or multiple iterations"""
    
    if mode == "single":
        # Single mode: one page only
        return await _run_single_page(url, provider)
    
    # For other modes, iterate through pages
    return await _run_multi_page(
        url=url,
        mode=mode,
        depth=depth,
        max_pages=max_pages,
        max_urls=max_urls,
        provider=provider,
    )


async def _run_single_page(url: str, provider: str):
    """Run a single page crawl"""
    
    from crawler_agent.nodes import get_crawler
    
    crawler = get_crawler(provider)
    result = await crawler.crawl(url)
    
    crawled_pages = [{
        "url": url,
        "markdown": result.get("markdown", ""),
        "html": result.get("html"),
        "links": result.get("links", []),
        "metadata": result.get("metadata", {}),
    }]
    
    return {
        "url": url,
        "mode": "single",
        "crawled_pages": crawled_pages,
        "visited_urls": [url],
        "extracted_links": result.get("links", []),
        "knowledge_graph": {"entities": [], "relationships": []},
        "status": "completed",
        "total_pages": 1,
    }


async def _run_multi_page(
    url: str,
    mode: str,
    depth: int,
    max_pages: int,
    max_urls: int,
    provider: str,
):
    """Run multi-page crawl with iteration"""
    
    from crawler_agent.nodes import get_crawler
    
    crawler = get_crawler(provider)
    
    # Initialize state
    crawled_pages = []
    visited_urls = []
    pending_urls = [url]
    extracted_links = []
    current_depth = 0
    
    max_iterations = min(max_pages, max_urls, 50)  # Safety limit
    
    while pending_urls and len(crawled_pages) < max_iterations:
        # Check depth limit
        if mode in ["depth", "knowledge"] and current_depth >= depth:
            break
        
        # Get next URL
        current_url = pending_urls.pop(0)
        
        # Skip if already visited
        if current_url in visited_urls:
            continue
        
        # Crawl the page
        try:
            result = await crawler.crawl(current_url)
            
            page_data = {
                "url": current_url,
                "markdown": result.get("markdown", ""),
                "html": result.get("html"),
                "links": result.get("links", []),
                "metadata": result.get("metadata", {}),
            }
            
            crawled_pages.append(page_data)
            visited_urls.append(current_url)
            current_depth += 1
            
            # Extract links for continuation (not for single mode)
            if mode in ["depth", "deep", "knowledge"]:
                new_links = [l for l in result.get("links", []) if l not in visited_urls]
                
                if mode == "depth":
                    # BFS: add limited links
                    pending_urls.extend(new_links[:5])
                elif mode == "deep":
                    # Deep: add more links
                    pending_urls.extend(new_links[:20])
                elif mode == "knowledge":
                    # Knowledge: extract relevant links
                    pending_urls.extend(_filter_relevant_links(new_links)[:3])
                
                extracted_links.extend(new_links)
                
        except Exception as e:
            print(f"Error crawling {current_url}: {e}")
            continue
    
    # Extract knowledge if needed
    knowledge_graph = {"entities": [], "relationships": []}
    if mode == "knowledge":
        knowledge_graph = _extract_kg_from_pages(crawled_pages)
    
    return {
        "url": url,
        "mode": mode,
        "depth": depth,
        "crawled_pages": crawled_pages,
        "visited_urls": visited_urls,
        "pending_urls": pending_urls,
        "extracted_links": extracted_links,
        "knowledge_graph": knowledge_graph,
        "status": "completed",
        "total_pages": len(crawled_pages),
        "current_depth": current_depth,
    }


def _filter_relevant_links(links: list) -> list:
    """Filter links likely to contain content"""
    
    excluded = [
        "login", "signin", "register", "signup",
        "logout", "signout",
        "contact", "about", "privacy", "terms",
        ".pdf", ".doc", ".docx", ".zip",
    ]
    
    return [l for l in links if not any(p in l.lower() for p in excluded)]


def _extract_kg_from_pages(pages: list) -> dict:
    """Extract knowledge graph from crawled pages"""
    
    entities = []
    relationships = []
    
    for page in pages:
        url = page.get("url", "")
        markdown = page.get("markdown", "")
        
        # Extract headings as entities
        for line in markdown.split("\n"):
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
    
    # Build relationships
    for i, entity in enumerate(entities):
        if i > 0 and entities[i-1]["type"] == "heading":
            relationships.append({
                "from": entities[i-1]["value"],
                "to": entity["value"],
                "type": "contains",
            })
    
    return {"entities": entities, "relationships": relationships}


# Export for external use
__all__ = ["create_crawl_graph", "run_crawl", "get_initial_state", "CrawlState"]