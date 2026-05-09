"""Crawler provider implementations"""
from crawler_agent.crawlers.firecrawl import FirecrawlCrawler
from crawler_agent.crawlers.crawl4ai import Crawl4AICrawler

__all__ = ["FirecrawlCrawler", "Crawl4AICrawler"]