"""Credit-based billing system"""
from typing import Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class CreditAccount:
    """Credit account for a user"""
    user_id: str
    credits: int = 0
    credits_used: int = 0
    total_spent: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @property
    def credits_remaining(self) -> int:
        return max(0, self.credits - self.credits_used)
    
    @property
    def utilization(self) -> float:
        if self.credits == 0:
            return 0.0
        return self.credits_used / self.credits


@dataclass  
class CreditPackage:
    """Credit packages for purchase"""
    name: str
    credits: int
    price: float
    bonus: int = 0
    
    @property
    def price_per_credit(self) -> float:
        total = self.credits + self.bonus
        if total == 0:
            return 0.0
        return self.price / total


# Credit packages available
CREDIT_PACKAGES = [
    CreditPackage(name="starter", credits=100, price=5.0, bonus=5),
    CreditPackage(name="basic", credits=500, price=20.0, bonus=50),
    CreditPackage(name="pro", credits=1000, price=35.0, bonus=150),
    CreditPackage(name="enterprise", credits=5000, price=150.0, bonus=1000),
]


# In-memory storage (use database in production)
_credit_accounts: Dict[str, CreditAccount] = {}


class CreditManager:
    """Manage user credits"""
    
    def __init__(self):
        self._accounts: Dict[str, CreditAccount] = {}
    
    def create_account(self, user_id: str, initial_credits: int = 0) -> CreditAccount:
        """Create new credit account"""
        account = CreditAccount(
            user_id=user_id,
            credits=initial_credits,
        )
        self._accounts[user_id] = account
        return account
    
    def get_account(self, user_id: str) -> Optional[CreditAccount]:
        """Get account"""
        return self._accounts.get(user_id)
    
    def add_credits(self, user_id: str, credits: int) -> CreditAccount:
        """Add credits to account"""
        account = self._accounts.get(user_id)
        if not account:
            account = self.create_account(user_id)
        
        account.credits += credits
        account.updated_at = datetime.now()
        return account
    
    def reserve_credits(self, user_id: str, credits_needed: int) -> bool:
        """Reserve credits for a crawl job"""
        account = self._accounts.get(user_id)
        if not account:
            return False
        
        return account.credits_remaining >= credits_needed
    
    def charge_credits(self, user_id: str, credits_used: int) -> bool:
        """Charge credits after crawl completes"""
        account = self._accounts.get(user_id)
        if not account:
            return False
        
        if account.credits_remaining < credits_used:
            return False
        
        account.credits_used += credits_used
        account.updated_at = datetime.now()
        return True
    
    def refund_credits(self, user_id: str, credits: int) -> bool:
        """Refund unused credits"""
        account = self._accounts.get(user_id)
        if not account:
            return False
        
        # Refund goes back to credit balance (not used)
        account.credits -= credits
        account.updated_at = datetime.now()
        return True


# Global credit manager instance
_credit_manager = CreditManager()


def get_credit_manager() -> CreditManager:
    """Get the global credit manager"""
    return _credit_manager


'''Simple billing - no calculation needed'''


# Just fixed credit cost per mode
CREDIT_COSTS = {}


def calculate_cost(mode: str, pages: int = 1, depth: int = 1) -> int:
    """Return 0 - currently free"""
    return 0


def calculate_llm_cost(provider: str, tokens_in: int, tokens_out: int) -> float:
    """Return 0 - currently free"""
    return 0.0


__all__ = [
    "CreditAccount",
    "CreditPackage", 
    "CREDIT_PACKAGES",
    "CreditManager",
    "get_credit_manager",
    "CREDIT_COSTS",
    "calculate_cost",
]