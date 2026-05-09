"""Subscription Plans for Crawling Service"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import os

# In production, use a database
_PLANS_DB: Dict[str, dict] = {}

@dataclass
class Plan:
    """Subscription plan definition"""
    name: str
    monthly_price: float
    pages_per_month: int
    max_depth: int
    allowed_modes: List[str]
    max_concurrent: int
    api_access: bool
    
    @property
    def pages_per_second(self) -> int:
        """Rate limit - pages per second"""
        return max(1, self.pages_per_month // 30_000)


# Define subscription plans
PLANS = {
    "free": Plan(
        name="free",
        monthly_price=0.0,
        pages_per_month=100,
        max_depth=1,
        allowed_modes=["single"],
        max_concurrent=1,
        api_access=False,
    ),
    "starter": Plan(
        name="starter",
        monthly_price=19.0,
        pages_per_month=1000,
        max_depth=2,
        allowed_modes=["single", "depth"],
        max_concurrent=2,
        api_access=True,
    ),
    "pro": Plan(
        name="pro",
        monthly_price=49.0,
        pages_per_month=10000,
        max_depth=5,
        allowed_modes=["single", "depth", "sitemap", "knowledge"],
        max_concurrent=5,
        api_access=True,
    ),
    "enterprise": Plan(
        name="enterprise",
        monthly_price=199.0,
        pages_per_month=-1,  # unlimited
        max_depth=-1,  # unlimited
        allowed_modes=["single", "depth", "sitemap", "knowledge", "deep"],
        max_concurrent=20,
        api_access=True,
    ),
}


def get_plan(name: str) -> Optional[Plan]:
    """Get plan by name"""
    return PLANS.get(name)


def can_use_mode(plan_name: str, mode: str) -> bool:
    """Check if plan allows this mode"""
    plan = get_plan(plan_name)
    if not plan:
        return False
    return mode in plan.allowed_modes


def can_reach_depth(plan_name: str, depth: int) -> bool:
    """Check if plan allows this depth"""
    plan = get_plan(plan_name)
    if not plan:
        return False
    if plan.max_depth == -1:
        return True
    return depth <= plan.max_depth


def has_pages_left(plan_name: str, used: int) -> bool:
    """Check if plan has pages remaining"""
    plan = get_plan(plan_name)
    if not plan:
        return False
    if plan.pages_per_month == -1:
        return True
    return used < plan.pages_per_month


# Plan pricing for display
PLAN_PRICING_DISPLAY = {
    "free": {"monthly": "$0", "per_page": "N/A"},
    "starter": {"monthly": "$19/mo", "per_page": "$0.019"},
    "pro": {"monthly": "$49/mo", "per_page": "$0.005"},
    "enterprise": {"monthly": "$199/mo", "per_page": "Negotiated"},
}


__all__ = [
    "PLANS", 
    "Plan", 
    "get_plan", 
    "can_use_mode", 
    "can_reach_depth",
    "has_pages_left",
    "PLAN_PRICING_DISPLAY",
]