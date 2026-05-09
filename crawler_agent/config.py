"""Crawler Agent Configuration"""
import os
from typing import Literal

# All available providers
CrawlProvider = Literal["firecrawl", "firecrawl-opensource", "crawl4ai"]
CrawlMode = Literal["single", "depth", "sitemap", "knowledge", "deep"]

# Default configurations
DEFAULT_MAX_PAGES = 50
DEFAULT_DEPTH = 2
DEFAULT_MAX_URLS = 100

# Provider configurations
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
FIRECRAWL_BASE_URL = os.getenv("FIRECRAWL_BASE_URL", "https://api.firecrawl.dev")

CRAWL4AI_CONFIG = {
    "headless": True,
    "verbose": True,
    "timeout": 30000,
    "max_concurrent": 3,
}

# Crawl modes description
CRAWL_MODE_DESCRIPTIONS = {
    "single": "Crawl exactly one URL - no recursive crawling",
    "depth": "Crawl starting URL and follows links up to specified depth",
    "sitemap": "Discover URLs from sitemap.xml and crawl all found URLs",
    "knowledge": "Crawl and extract structured knowledge graph",
    "deep": "Recursively crawl ALL links until end nodes",
}