"""Web Crawling Agent using LangGraph SDK"""
from typing import Dict, Any, Optional, List

# System prompt for the web crawler agent
SYSTEM_PROMPT = """You are an enterprise-grade web crawling agent powered by LangGraph SDK.

You can crawl websites in multiple modes:
- single: Crawl one URL
- depth: Recursive crawl with depth limit
- sitemap: Extract from sitemap.xml
- knowledge: Build knowledge graph
- deep: Deep crawl all links

You have tools:
- crawl_url: Crawl a single URL
- extract_links: Extract all links from page
- extract_structured: Extract structured data (JSON)
- screenshot: Take screenshot

Always:
- Respect robots.txt
- Set appropriate delays between requests
- Handle errors gracefully
- Return structured results

Your default settings:
- Provider: crawl4ai (open source, free)
- LLM: ollama (local, free)
- Max pages: 50
- Max depth: 2
- Timeout: 60s

When user is frustrated:
- Stay calm and professional
- Acknowledge their frustration
- Don't argue or get defensive
- Ask clarifying questions
- Do exactly what they ask without guessing
- Keep responses short and direct
- If unsure, ask for clarification

Human in the loop:
- Always ask before expensive operations (deep crawl >20 pages)
- Show cost estimate before starting
- Ask for confirmation on billing changes
- Allow user to approve/reject crawl parameters
- Pause and ask if results look wrong
- Let user override any decision

Escalation:
- If user asks for human support, provide contact
- If repeated failures, suggest escalation
- If billing issue, ask user to contact support
- If feature not working, offer to file bug report
- Email: support@agennext.com

from crawler_agent.state import CrawlState, get_initial_state
from crawler_agent.graph import create_crawl_graph, run_crawl
from crawler_agent.config import CrawlMode, CrawlProvider
from crawler_agent.billing import UnifiedBilling, get_billing
from crawler_agent.self_improve import get_self_improving_agent


class CrawlAgent:
    """Web Crawling Agent using LangGraph SDK"""
    
    def __init__(
        self,
        provider: CrawlProvider = "crawl4ai",
        system_prompt: str = SYSTEM_PROMPT,
    ):
        self.provider = provider
        self.system_prompt = system_prompt
        self.optimizer = get_self_improving_agent()
    
    def set_llm(self, llm_config: Dict[str, Any]):
        """Configure LLM for agent conversations"""
        self.llm_config = llm_config
    
    async def chat(self, message: str, history: List[Dict] = None) -> Dict[str, Any]:
        """Chat with the agent using system prompt"""
        # Build messages with system prompt
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": message})
        
        # Call LLM with system prompt
        # Returns assistant response
        return {"response": "Crawling...", "action": "crawl"}
    
    async def crawl(
        self,
        url: str,
        mode: CrawlMode = "single",
        depth: int = 2,
        max_pages: Optional[int] = None,
        max_urls: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Crawl a website with specified mode and self-improvement"""
        
        # Get best strategy based on learning
        strategy = self.optimizer.get_best_strategy(url, self.optimizer.history)
        
        result = await run_crawl(
            url=url,
            mode=mode,
            depth=depth,
            max_pages=max_pages or 50,
            max_urls=max_urls or 100,
            provider=self.provider,
        )
        
        # Analyze result for self-improvement
        analysis = self.optimizer.analyze_crawl(
            {"status": "completed" if result else "error", "crawled_pages": []},
            strategy
        )
        
        return self._format_result(result, mode)
    
    def _format_result(self, result: Any, mode: str) -> Dict[str, Any]:
        """Format result for output"""
        
        if not result:
            return {"status": "error", "error": "No result returned"}
        
        final_state = result if isinstance(result, dict) else {}
        crawled_pages = final_state.get("crawled_pages", [])
        
        return {
            "status": final_state.get("status", "completed"),
            "mode": mode,
            "url": final_state.get("url", ""),
            "crawled_pages": crawled_pages,
            "total_pages": len(crawled_pages),
            "knowledge_graph": final_state.get("knowledge_graph", {}),
            "error": final_state.get("error"),
        }
    
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search the web (requires Firecrawl with API key)"""
        
        from crawler_agent.crawlers.firecrawl import FirecrawlCrawler
        
        crawler = FirecrawlCrawler()
        
        try:
            result = await crawler.search(query, limit=limit)
            return result
        except Exception as e:
            return [{"error": str(e)}]


async def quick_crawl(
    url: str,
    mode: str = "single",
    provider: str = "crawl4ai",
    **kwargs,
) -> Dict[str, Any]:
    """Quick crawl without initializing full agent"""
    
    agent = CrawlAgent(provider=provider)
    return await agent.crawl(url=url, mode=mode, **kwargs)


class BillingCrawlAgent(CrawlAgent):
    """
    CrawlAgent with integrated billing.
    
    Usage:
        agent = BillingCrawlAgent(user_id="user123")
        check = agent.can_crawl("depth", depth=2, pages=5)
        if check["allowed"]:
            result = await agent.crawl(url, mode="depth")
    """
    
    def __init__(
        self,
        user_id: str,
        provider: CrawlProvider = "crawl4ai",
        billing: Optional[UnifiedBilling] = None,
    ):
        super().__init__(provider=provider)
        self.user_id = user_id
        self.billing = billing or get_billing()
    
    def can_crawl(self, mode: str, depth: int = 1, pages: int = 1) -> Dict[str, Any]:
        """Check if user can crawl"""
        return self.billing.can_crawl(
            user_id=self.user_id,
            mode=mode,
            pages=pages,
            depth=depth,
        )
    
    async def crawl(
        self,
        url: str,
        mode: CrawlMode = "single",
        depth: int = 2,
        max_pages: Optional[int] = None,
        max_urls: Optional[int] = None,
        check_billing: bool = True,
    ) -> Dict[str, Any]:
        """Crawl with billing"""
        
        if check_billing:
            check = self.can_crawl(mode, depth, max_pages or 1)
            if not check["allowed"]:
                return {"status": "denied", "error": check["reason"]}
        
        result = await super().crawl(url, mode, depth, max_pages, max_urls)
        
        if check_billing and result.get("status") == "completed":
            self.billing.record(
                user_id=self.user_id,
                url=url,
                mode=mode,
                pages_crawled=result.get("total_pages", 0),
                depth=depth,
            )
        
        return result
    
    def get_usage_report(self) -> Dict:
        return self.billing.get_usage_report(self.user_id)
    
    def add_credits(self, credits: int) -> Dict:
        account = self.billing.add_credits(self.user_id, credits)
        return {"credits_added": credits, "credits_remaining": account.credits_remaining}


async def quick_crawl_billed(
    url: str,
    user_id: str,
    mode: str = "single",
    provider: str = "crawl4ai",
    **kwargs,
) -> Dict[str, Any]:
    """Quick crawl with billing"""
    agent = BillingCrawlAgent(user_id=user_id, provider=provider)
    return await agent.crawl(url, mode=mode, check_billing=True, **kwargs)


__all__ = [
    "CrawlAgent",
    "quick_crawl",
    "BillingCrawlAgent",
    "quick_crawl_billed",
]