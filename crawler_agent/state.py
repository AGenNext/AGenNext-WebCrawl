"""Crawler Agent State Definitions"""
from typing import TypedDict, Optional, List, Dict, Any
from crawler_agent.config import CrawlMode, CrawlProvider


class CrawledPage(TypedDict):
    """Single crawled page data"""
    url: str
    markdown: str
    html: Optional[str]
    links: List[str]
    metadata: Dict[str, Any]


class CrawlState(TypedDict):
    """State that flows through the crawling graph"""
    # Input parameters
    url: str
    mode: CrawlMode
    depth: int
    max_pages: Optional[int]
    max_urls: Optional[int]
    provider: CrawlProvider
    
    # Crawling state
    crawled_pages: List[CrawledPage]
    visited_urls: List[str]
    pending_urls: List[str]
    extracted_links: List[str]
    
    # Knowledge graph (for knowledge mode)
    knowledge_graph: Dict[str, Any]
    
    # Status and errors
    status: str
    error: Optional[str]
    
    # Statistics
    total_pages: int
    current_depth: int


def get_initial_state(
    url: str,
    mode: CrawlMode = "single",
    depth: int = 2,
    max_pages: Optional[int] = None,
    max_urls: Optional[int] = None,
    provider: CrawlProvider = "firecrawl",
) -> CrawlState:
    """Create initial state for the crawling graph"""
    return CrawlState(
        url=url,
        mode=mode,
        depth=depth,
        max_pages=max_pages,
        max_urls=max_urls,
        provider=provider,
        crawled_pages=[],
        visited_urls=[],
        pending_urls=[url],
        extracted_links=[],
        knowledge_graph={"entities": [], "relationships": []},
        status="running",
        error=None,
        total_pages=0,
        current_depth=0,
    )