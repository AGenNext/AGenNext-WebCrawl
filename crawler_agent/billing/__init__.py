"""
Crawler Agent Billing Module

Provides 3 billing methods:
1. Credits - Prepaid credit system
2. Plans - Subscription tiers
3. Usage - Pay-per-use metering

Usage:
    from crawler_agent.billing import CreditBilling, PlanBilling, UsageBilling
    
    # Or use unifiedBilling for all three
    from crawler_agent.billing import UnifiedBilling
    
    billing = UnifiedBilling()
    
    # Check access before crawling
    if billing.can_crawl(user_id="user123", mode="depth", depth=2):
        result = await agent.crawl(url, mode="depth", depth=2)
        billing.record(user_id="user123", result=result)
"""
from typing import Optional, Dict
from crawler_agent.billing.plans import PLANS, get_plan, can_use_mode, PLAN_PRICING_DISPLAY
from crawler_agent.billing.credits import (
    CreditManager,
    CreditAccount,
    CREDIT_PACKAGES,
    calculate_cost,
    get_credit_manager,
)
from crawler_agent.billing.usage import (
    UsageTracker,
    MonthlyUsage,
    get_usage_tracker,
    RATE_CARDS,
    get_rate,
)


class UnifiedBilling:
    """
    Unified billing that supports all three methods.
    
    Priority: Credits > Subscription > Usage (metered)
    """
    
    def __init__(self):
        self.credit_manager = get_credit_manager()
        self.usage_tracker = get_usage_tracker()
    
    # === Subscription Checks ===
    
    def get_subscription(self, user_id: str) -> Optional[str]:
        """Get user's subscription plan name"""
        # In production, check database
        # For demo, check environment
        import os
        plan = os.getenv(f"USER_PLAN_{user_id}", "free")
        return plan
    
    def has_subscription(self, user_id: str) -> bool:
        """Check if user has paid subscription"""
        plan = self.get_subscription(user_id)
        return plan and plan != "free"
    
    def can_use_mode(self, user_id: str, mode: str) -> bool:
        """Check if subscription allows mode"""
        plan = self.get_subscription(user_id)
        from crawler_agent.billing.plans import can_use_mode as check
        return check(plan, mode)
    
    def can_reach_depth(self, user_id: str, depth: int) -> bool:
        """Check if subscription allows depth"""
        plan = self.get_subscription(user_id)
        from crawler_agent.billing.plans import can_reach_depth as check
        return check(plan, depth)
    
    # === Credit Checks ===
    
    def get_credits(self, user_id: str) -> int:
        """Get user's credit balance"""
        account = self.credit_manager.get_account(user_id)
        return account.credits_remaining if account else 0
    
    def has_credits(self, user_id: str, amount: int) -> bool:
        """Check if user has enough credits"""
        return self.credit_manager.reserve_credits(user_id, amount)
    
    # === Combined Access Check ===
    
    def can_crawl(
        self,
        user_id: str,
        mode: str,
        pages: int = 1,
        depth: int = 1,
    ) -> Dict[str, any]:
        """
        Check if user can perform crawl.
        
        Returns:
            {"allowed": bool, "reason": str, "method": str}
        """
        # 1. Check subscription first
        if self.has_subscription(user_id):
            plan = self.get_subscription(user_id)
            if not self.can_use_mode(user_id, mode):
                return {
                    "allowed": False,
                    "reason": f"Mode '{mode}' not in plan '{plan}'",
                    "method": "subscription",
                }
            if not self.can_reach_depth(user_id, depth):
                return {
                    "allowed": False,
                    "reason": f"Depth {depth} exceeds plan limit",
                    "method": "subscription",
                }
            return {
                "allowed": True,
                "reason": "",
                "method": "subscription",
                "plan": plan,
            }
        
        # 2. Check credits for free tier
        cost = calculate_cost(mode, pages, depth)
        if self.has_credits(user_id, cost):
            return {
                "allowed": True,
                "reason": "",
                "method": "credits",
                "cost": cost,
            }
        
        # 3. Check usage for metered access (if enabled)
        # For now, deny if no credits
        return {
            "allowed": False,
            "reason": "No credits or subscription",
            "method": "none",
        }
    
    # === Recording ===
    
    def record(
        self,
        user_id: str,
        url: str,
        mode: str,
        pages_crawled: int,
        links_found: int = 0,
        depth: int = 1,
    ):
        """Record a completed crawl for billing"""
        # Track usage
        self.usage_tracker.record_crawl(
            user_id=user_id,
            url=url,
            mode=mode,
            pages_crawled=pages_crawled,
            links_found=links_found,
        )
        
        # Charge credits if on free tier
        if not self.has_subscription(user_id):
            cost = calculate_cost(mode, pages_crawled, depth)
            self.credit_manager.charge_credits(user_id, cost)
    
    # === Add Credits ===
    
    def add_credits(self, user_id: str, credits: int, payment: float = 0.0):
        """Add credits to user account"""
        account = self.credit_manager.add_credits(user_id, credits)
        return account
    
    # === Reporting ===
    
    def get_usage_report(self, user_id: str) -> Dict:
        """Get user's usage report"""
        monthly = self.usage_tracker.get_monthly_usage(user_id)
        stats = self.usage_tracker.get_usage_stats(user_id)
        
        return {
            "user_id": user_id,
            "subscription": self.get_subscription(user_id),
            "credits_remaining": self.get_credits(user_id),
            "current_month": {
                "pages": monthly.total_pages if monthly else 0,
                "calls": monthly.total_calls if monthly else 0,
            } if monthly else {"pages": 0, "calls": 0},
            "all_time": stats,
        }


# Default instance
_default_billing = UnifiedBilling()


def get_billing() -> UnifiedBilling:
    """Get default billing instance"""
    return _default_billing


__all__ = [
    # Plans
    "PLANS",
    "get_plan",
    "can_use_mode",
    "PLAN_PRICING_DISPLAY",
    
    # Credits
    "CreditManager",
    "CreditAccount",
    "CREDIT_PACKAGES",
    "calculate_cost",
    "get_credit_manager",
    
    # Usage
    "UsageTracker",
    "MonthlyUsage",
    "get_usage_tracker",
    "RATE_CARDS",
    "get_rate",
    
    # Unified
    "UnifiedBilling",
    "get_billing",
]