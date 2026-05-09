"""Crawl4AI crawler implementation"""
from typing import Dict, Any, List, Optional
import httpx

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawler_agent.config import CRAWL4AI_CONFIG


class Crawl4AICrawler:
    """Crawl4AI open-source crawler implementation"""
    
    def __init__(self, **config):
        self.config = {**CRAWL4AI_CONFIG, **config}
    
    async def crawl(self, url: str) -> Dict[str, Any]:
        """Crawl a single URL using Crawl4AI"""
        
        run_config = CrawlerRunConfig(
            wait_for=self.config.get("wait_for"),
        )
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
                config=run_config,
            )
            
            if result.success:
                links = self._extract_links(result.html)
                
                return {
                    "url": url,
                    "markdown": result.markdown,
                    "html": result.html,
                    "links": links,
                    "metadata": {
                        "title": result.metadata.get("title", "") if result.metadata else "",
                        "description": result.metadata.get("description", "") if result.metadata else "",
                    },
                }
            else:
                return {
                    "url": url,
                    "markdown": "",
                    "html": "",
                    "links": [],
                    "error": getattr(result, 'error_message', 'Unknown error'),
                }
    
    def _extract_links(self, html: str) -> List[str]:
        """Extract all HTTP links from HTML content"""
        from bs4 import BeautifulSoup
        
        if not html:
            return []
            
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for a in soup.find_all('a', href=True):
            href = a.get('href', '')
            # Only include absolute HTTP URLs
            if href.startswith('http'):
                links.append(href)
        
        return links
    
    async def crawl_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Crawl multiple URLs"""
        results = []
        for url in urls:
            result = await self.crawl(url)
            results.append(result)
        return results