"""Usage tracking and metering for billing"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict


@dataclass
class CrawlUsage:
    """Single crawl usage record"""
    timestamp: datetime = field(default_factory=datetime.now)
    url: str = ""
    mode: str = ""
    pages_crawled: int = 0
    links_found: int = 0
    data_mb: float = 0.0
    duration_ms: int = 0
    # LLM Token usage
    tokens_in: int = 0
    tokens_out: int = 0
    llm_provider: str = ""
    llm_model: str = ""


@dataclass
class MonthlyUsage:
    """Monthly usage summary"""
    year: int
    month: int
    total_pages: int = 0
    total_links: int = 0
    total_calls: int = 0
    data_mb: float = 0.0
    cost_usd: float = 0.0
    # LLM token totals
    total_tokens_in: int = 0
    total_tokens_out: int = 0
    
    @property
    def total_tokens(self) -> int:
        return self.total_tokens_in + self.total_tokens_out
    
    @property
    def period(self) -> str:
        return f"{self.year}-{self.month:02d}"


class UsageTracker:
    """Track API usage for metering/billing"""
    
    def __init__(self):
        self._usage: Dict[str, List[CrawlUsage]] = defaultdict(list)
        self._monthly: Dict[str, MonthlyUsage] = {}
    
    def record_crawl(
        self,
        user_id: str,
        url: str,
        mode: str,
        pages_crawled: int,
        links_found: int = 0,
        data_bytes: int = 0,
        duration_ms: int = 0,
    ):
        """Record a crawl operation"""
        # Create usage record
        usage = CrawlUsage(
            url=url,
            mode=mode,
            pages_crawled=pages_crawled,
            links_found=links_found,
            data_mb=data_bytes / (1024 * 1024),
            duration_ms=duration_ms,
        )
        
        self._usage[user_id].append(usage)
        
        # Update monthly aggregate
        now = datetime.now()
        period_key = f"{now.year}-{now.month:02d}"
        user_period = f"{user_id}:{period_key}"
        
        if user_period not in self._monthly:
            self._monthly[user_period] = MonthlyUsage(now.year, now.month)
        
        monthly = self._monthly[user_period]
        monthly.total_pages += pages_crawled
        monthly.total_links += links_found
        monthly.total_calls += 1
        monthly.data_mb += data_bytes / (1024 * 1024)
    
    def get_user_usage(
        self, 
        user_id: str, 
        hours: int = 24
    ) -> List[CrawlUsage]:
        """Get recent usage for user"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            u for u in self._usage[user_id]
            if u.timestamp >= cutoff
        ]
    
    def get_monthly_usage(
        self, 
        user_id: str, 
        year: int = None,
        month: int = None
    ) -> Optional[MonthlyUsage]:
        """Get monthly usage summary"""
        if year is None:
            now = datetime.now()
            year = now.year
        if month is None:
            month = now.month
        
        period_key = f"{user_id}:{year}-{month:02d}"
        return self._monthly.get(period_key)
    
    def get_usage_stats(self, user_id: str) -> Dict:
        """Get overall usage statistics"""
        all_usage = self._usage.get(user_id, [])
        
        return {
            "total_crawls": len(all_usage),
            "total_pages": sum(u.pages_crawled for u in all_usage),
            "total_links": sum(u.links_found for u in all_usage),
            "modes_used": list(set(u.mode for u in all_usage)),
            "first_crawl": all_usage[0].timestamp if all_usage else None,
            "last_crawl": all_usage[-1].timestamp if all_usage else None,
        }
    
    def generate_invoice(
        self,
        user_id: str,
        rate_per_page: float = 0.01,
        year: int = None,
        month: int = None
    ) -> MonthlyUsage:
        """Generate invoice data for a period"""
        usage = self.get_monthly_usage(user_id, year, month)
        
        if usage:
            usage.cost_usd = usage.total_pages * rate_per_page
        
        return usage


# Global usage tracker
_usage_tracker = UsageTracker()


def get_usage_tracker() -> UsageTracker:
    """Get the global usage tracker"""
    return _usage_tracker


# Rate cards (price per page)
RATE_CARDS = {
    "free": 0.0,
    "default": 0.01,
    "volume": 0.008,  # >10k pages
    "enterprise": 0.005,
}


def get_rate(tier: str = "default") -> float:
    """Get rate for tier"""
    return RATE_CARDS.get(tier, 0.01)


__all__ = [
    "CrawlUsage",
    "MonthlyUsage", 
    "UsageTracker",
    "get_usage_tracker",
    "RATE_CARDS",
    "get_rate",
    "generate_invoice",
]