"""Web Crawling Agent using LangGraph SDK

This package provides a comprehensive web crawling agent using LangGraph SDK
with support for Firecrawl and Crawl4AI open-source APIs.

Crawl Modes:
- single: Crawl exactly one URL
- depth: Crawl with depth-limited traversal
- sitemap: Crawl URLs from sitemap.xml
- knowledge: Extract knowledge graph
- deep: Deep crawl all links

Usage:
    from crawler_agent import CrawlAgent, quick_crawl
    
    # Quick single page crawl
    result = await quick_crawl("https://example.com")
    
    # Full agent with custom LLM
    agent = CrawlAgent(llm=my_llm, provider="crawl4ai")
    result = await agent.crawl("https://example.com", mode="depth", depth=2)
"""
from crawler_agent.agent import CrawlAgent, quick_crawl, BillingCrawlAgent, quick_crawl_billed
from crawler_agent.state import CrawlState, get_initial_state
from crawler_agent.graph import create_crawl_graph, run_crawl
from crawler_agent.config import CrawlMode, CrawlProvider

# Billing exports
from crawler_agent.billing import (
    UnifiedBilling,
    get_billing,
    PLANS,
    CreditAccount,
    CREDIT_PACKAGES,
    calculate_cost,
    UsageTracker,
    get_rate,
)

__version__ = "0.1.0"

__all__ = [
    # Core
    "CrawlAgent",
    "quick_crawl",
    "run_crawl",
    "CrawlState",
    "get_initial_state",
    "create_crawl_graph",
    "CrawlMode",
    "CrawlProvider",
    # Billing
    "BillingCrawlAgent",
    "quick_crawl_billed",
    "UnifiedBilling",
    "get_billing",
    "PLANS",
    "CreditAccount",
    "CREDIT_PACKAGES",
    "calculate_cost",
    "UsageTracker",
    "get_rate",
]