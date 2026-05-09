"""Firecrawl crawler - supports both cloud API and open-source"""
from typing import Dict, Any, List, Optional
import os

# Try to import firecrawl package for cloud API
try:
    from firecrawl import Firecrawl as FirecrawlCloud
    FIRECRAWL_CLOUD_AVAILABLE = True
except ImportError:
    FIRECRAWL_CLOUD_AVAILABLE = False

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig


class FirecrawlCrawler:
    """
    Firecrawl crawler with two modes:
    1. Cloud API (requires API key) - more features, structured extraction
    2. Open-source (no API key) - uses Crawl4AI engine
    
    Usage:
        # Without API key (uses opensource)
        crawler = FirecrawlCrawler()
        
        # With API key (uses cloud when available)
        crawler = FirecrawlCrawler(api_key="fc-...")
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.firecrawl.dev"):
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY", "")
        self.base_url = base_url
        self._cloud_client = None
        
        # Determine mode
        if self.api_key and FIRECRAWL_CLOUD_AVAILABLE:
            self._mode = "cloud"
        else:
            self._mode = "opensource"
    
    @property
    def mode(self) -> str:
        """Returns 'cloud' or 'opensource'"""
        return self._mode
    
    async def crawl(self, url: str) -> Dict[str, Any]:
        """Crawl a URL using Firecrawl"""
        
        if self._mode == "cloud" and self.api_key:
            return await self._crawl_cloud(url)
        else:
            return await self._crawl_opensource(url)
    
    async def _crawl_cloud(self, url: str) -> Dict[str, Any]:
        """Use Firecrawl cloud API"""
        
        if not self._cloud_client:
            self._cloud_client = FirecrawlCloud(
                api_key=self.api_key,
                base_url=self.base_url
            )
        
        try:
            result = self._cloud_client.scrape_url(url)
            
            if result.success:
                links = self.extract_links(result.html)
                
                return {
                    "url": url,
                    "markdown": result.markdown,
                    "html": result.html,
                    "links": links,
                    "metadata": result.metadata or {},
                }
            else:
                return {
                    "url": url,
                    "markdown": "",
                    "html": "",
                    "links": [],
                    "error": result.error,
                }
                
        except Exception as e:
            print(f"Firecrawl cloud failed, falling back to opensource: {e}")
            return await self._crawl_opensource(url)
    
    async def _crawl_opensource(self, url: str) -> Dict[str, Any]:
        """Use Crawl4AI as opensource engine"""
        
        run_config = CrawlerRunConfig(wait_for=None)
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if result.success:
                links = self.extract_links(result.html)
                
                return {
                    "url": url,
                    "markdown": result.markdown,
                    "html": result.html,
                    "links": links,
                    "metadata": result.metadata or {},
                }
            else:
                return {
                    "url": url,
                    "markdown": "",
                    "html": "",
                    "links": [],
                    "error": getattr(result, 'error_message', 'Unknown error'),
                }
    
    async def crawl_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Crawl multiple URLs"""
        results = []
        for url in urls:
            result = await self.crawl(url)
            results.append(result)
        return results
    
    def extract_links(self, html: str) -> List[str]:
        """Extract all links from HTML content"""
        from bs4 import BeautifulSoup
        
        if not html:
            return []
            
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for a in soup.find_all('a', href=True):
            href = a.get('href', '')
            if href.startswith('http'):
                links.append(href)
            elif href.startswith('/'):
                links.append(href)
        
        return links