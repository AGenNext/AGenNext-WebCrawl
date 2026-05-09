"""Self-Improving Agent for Web Crawler

Analyzes performance, learns from errors, and optimizes crawl strategies.
"""
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class SelfImprovingAgent:
    """Agent that learns and improves from crawl experiences"""
    
    def __init__(self):
        # Performance history
        self.history: List[Dict[str, Any]] = []
        self.success_strategies: Dict[str, List[str]] = defaultdict(list)
        self.error_patterns: Dict[str, int] = defaultdict(int)
        
        # Strategy templates
        self.strategies = {
            "single": {
                "timeout": 30,
                "wait_for": None,
                "javascript": False,
            },
            "with_js": {
                "timeout": 60,
                "wait_for": "networkidle",
                "javascript": True,
            },
            "retry": {
                "max_retries": 3,
                "backoff": 2,
            },
            "sitemap": {
                "priority": "xml,html",
            },
        }
    
    def analyze_crawl(self, result: Dict[str, Any], strategy: str) -> Dict[str, Any]:
        """Analyze crawl result and determine improvements"""
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "strategy": strategy,
            "success": result.get("status") == "completed",
            "pages_found": len(result.get("crawled_pages", [])),
            "errors": result.get("errors", []),
        }
        
        # Extract error patterns
        for error in result.get("errors", []):
            error_type = self._classify_error(error)
            self.error_patterns[error_type] += 1
        
        # Record successful strategies
        if analysis["success"] and strategy:
            self.success_strategies[strategy].append(analysis["timestamp"])
        
        self.history.append(analysis)
        
        return self._generate_recommendations(analysis)
    
    def _classify_error(self, error: str) -> str:
        """Classify error into category"""
        error_lower = error.lower()
        
        if "timeout" in error_lower:
            return "timeout"
        elif "403" in error_lower or "forbidden" in error_lower:
            return "auth_required"
        elif "404" in error_lower:
            return "not_found"
        elif "500" in error_lower:
            return "server_error"
        elif "javascript" in error_lower:
            return "js_required"
        elif "connection" in error_lower:
            return "network_error"
        else:
            return "unknown"
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategy recommendations based on patterns"""
        
        recommendations = {
            "current_strategy": analysis["strategy"],
            "suggested_strategy": None,
            "optimizations": [],
            "confidence": 0.0,
        }
        
        # Check error patterns
        error_types = list(self.error_patterns.keys())
        
        if "timeout" in error_types:
            recommendations["suggested_strategy"] = "with_js"
            recommendations["optimizations"].append("Increase timeout for slow pages")
        
        if "js_required" in error_types:
            recommendations["suggested_strategy"] = "with_js"
            recommendations["optimizations"].append("Enable JavaScript rendering")
        
        if "auth_required" in error_types:
            recommendations["optimizations"].append("Add user-agent rotation")
            recommendations["optimizations"].append("Add rate limiting")
        
        if "network_error" in error_types:
            recommendations["suggested_strategy"] = "retry"
            recommendations["optimizations"].append("Add retry with exponential backoff")
        
        # Calculate confidence based on history
        if self.history:
            successful = sum(1 for h in self.history if h["success"])
            recommendations["confidence"] = successful / len(self.history)
        
        return recommendations
    
    def get_best_strategy(self, url: str, past_results: List[Dict]) -> str:
        """Determine best strategy based on URL patterns and history"""
        
        # Check URL characteristics
        if self._is_sitemap_likely(url):
            return "sitemap"
        elif self._requires_js(url):
            return "with_js"
        
        # Check history for similar URLs
        for result in past_results[-5:]:
            if result.get("success"):
                return result.get("strategy", "single")
        
        return "single"
    
    def _is_sitemap_likely(self, url: str) -> bool:
        """Check if URL likely has sitemap"""
        return "/blog" in url or "/news" in url or "/posts" in url
    
    def _requires_js(self, url: str) -> bool:
        """Check if URL likely requires JavaScript"""
        js_frameworks = ["react", "vue", "angular", "next.js", "nuxt"]
        return any(f in url.lower() for f in js_frameworks)
    
    def apply_improvements(self, base_config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply learned improvements to config"""
        
        improved = base_config.copy()
        
        for error_type, count in self.error_patterns.items():
            if count > 2:
                if error_type == "timeout":
                    improved["timeout"] = min(improved.get("timeout", 30) * 2, 120)
                elif error_type == "network_error":
                    improved["max_retries"] =improved.get("max_retries", 1) + 1
        
        return improved
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        
        return {
            "total_crawls": len(self.history),
            "successful_crawls": sum(1 for h in self.history if h["success"]),
            "success_rate": sum(1 for h in self.history if h["success"]) / max(len(self.history), 1),
            "error_patterns": dict(self.error_patterns),
            "strategies_used": dict(self.success_strategies),
        }


# Global instance
_agent: Optional[SelfImprovingAgent] = None


def get_self_improving_agent() -> SelfImprovingAgent:
    """Get or create global self-improving agent"""
    global _agent
    if _agent is None:
        _agent = SelfImprovingAgent()
    return _agent


async def analyze_and_optimize(
    result: Dict[str, Any],
    strategy: str,
) -> Dict[str, Any]:
    """Analyze crawl and return optimized config"""
    
    agent = get_self_improving_agent()
    
    # Analyze result
    analysis = agent.analyze_crawl(result, strategy)
    
    # Get recommendations
    recommendations = agent._generate_recommendations(analysis)
    
    # Apply if high confidence
    if recommendations["confidence"] > 0.7:
        return {
            "strategy": recommendations.get("suggested_strategy", strategy),
            "config": agent.apply_improvements({}),
            "analysis": analysis,
        }
    
    return {
        "strategy": strategy,
        "config": {},
        "analysis": analysis,
    }