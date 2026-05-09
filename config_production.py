"""Production Configuration

Production-hardened settings for Web Crawler Agent.
"""
import os
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ProductionConfig:
    """Production application configuration"""
    
    # App Identity
    APP_NAME: str = "Web Crawler Agent"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8501
    
    # Security - MUST CHANGE IN PRODUCTION
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")
    ALLOWED_HOSTS: str = os.environ.get("ALLOWED_HOSTS", "*")
    CORS_ORIGINS: str = os.environ.get("CORS_ORIGINS", "")
    ENABLE_CORS: bool = False
    ENABLE_XSRF: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "60"))
    RATE_LIMIT_PER_HOUR: int = int(os.environ.get("RATE_LIMIT_PER_HOUR", "1000"))
    MAX_CONCURRENT_CRAWLS: int = int(os.environ.get("MAX_CONCURRENT_CRAWLS", "5"))
    
    # Crawl Limits
    MAX_PAGES_PER_CRAWL: int = int(os.environ.get("MAX_PAGES_PER_CRAWL", "1000"))
    MAX_DEPTH: int = int(os.environ.get("MAX_DEPTH", "5"))
    CRAWL_TIMEOUT: int = int(os.environ.get("CRAWL_TIMEOUT", "300"))
    MAX_PAGE_SIZE_MB: int = int(os.environ.get("MAX_PAGE_SIZE_MB", "10"))
    
    # Providers - API Keys
    DEFAULT_PROVIDER: str = os.environ.get("DEFAULT_PROVIDER", "crawl4ai")
    FIRECRAWL_API_KEY: Optional[str] = os.environ.get("FIRECRAWL_API_KEY")
    CRAWL4AI_API_KEY: Optional[str] = os.environ.get("CRAWL4AI_API_KEY")
    JINA_API_KEY: Optional[str] = os.environ.get("JINA_API_KEY")
    
    # Billing
    FREE_CREDITS: int = int(os.environ.get("FREE_CREDITS", "100"))
    CREDIT_PER_PAGE: float = float(os.environ.get("CREDIT_PER_PAGE", "0.01"))
    MAX_CREDITS_PER_USER: int = int(os.environ.get("MAX_CREDITS_PER_USER", "100000"))
    
    # Logging
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "WARNING")
    LOG_FILE: str = os.environ.get("LOG_FILE", "/var/log/crawler-agent.log")
    ENABLE_ACCESS_LOG: bool = True
    
    # Monitoring
    ENABLE_METRICS: bool = os.environ.get("ENABLE_METRICS", "true").lower() == "true"
    HEALTH_CHECK_PATH: str = "/_stcore/health"
    METRICS_PORT: int = 9090
    
    # Session
    SESSION_TIMEOUT_HOURS: int = int(os.environ.get("SESSION_TIMEOUT_HOURS", "24"))
    MAX_SESSIONS_PER_USER: int = int(os.environ.get("MAX_SESSIONS_PER_USER", "3"))
    
    # Database (optional)
    DATABASE_URL: Optional[str] = os.environ.get("DATABASE_URL")
    
    # Redis (optional)
    REDIS_URL: Optional[str] = os.environ.get("REDIS_URL")
    
    # Feature Flags
    ENABLE_CHAT_UI: bool = os.environ.get("ENABLE_CHAT_UI", "true").lower() == "true"
    ENABLE_BILLING: bool = os.environ.get("ENABLE_BILLING", "true").lower() == "true"
    ENABLE_API: bool = os.environ.get("ENABLE_API", "true").lower() == "true"
    
    def validate(self) -> list:
        """Validate configuration, return list of warnings"""
        warnings = []
        
        if self.DEBUG:
            warnings.append("WARNING: DEBUG is enabled!")
        
        if self.SECRET_KEY == "CHANGE_ME_IN_PRODUCTION":
            warnings.append("ERROR: SECRET_KEY not set!")
        
        if self.CORS_ORIGINS == "*":
            warnings.append("WARNING: CORS allows all origins")
        
        return warnings


# Production security headers
SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}


# Rate limiter
class RateLimiter:
    """IP-based rate limiter"""
    
    def __init__(self, per_minute: int = 60, per_hour: int = 1000):
        self.per_minute = per_minute
        self.per_hour = per_hour
        self.minute_requests = {}
        self.hourly_requests = {}
    
    def check(self, ip: str) -> tuple:
        """
        Check if request is allowed.
        Returns (allowed: bool, remaining_minute: int, remaining_hour: int)
        """
        import time
        now = int(time.time())
        
        # Clean old entries
        self.minute_requests = {k: v for k, v in self.minute_requests.items() if now - v[1] < 60}
        self.hourly_requests = {k: v for k, v in self.hourly_requests.items() if now - v[1] < 3600}
        
        # Calculate remaining
        minute_used = self.minute_requests.get(ip, (0, 0))[0]
        hour_used = self.hourly_requests.get(ip, (0, 0))[0]
        
        remaining_min = max(0, self.per_minute - minute_used)
        remaining_hour = max(0, self.per_hour - hour_used)
        
        if minute_used >= self.per_minute or hour_used >= self.per_hour:
            return False, remaining_min, remaining_hour
        
        # Record
        self.minute_requests[ip] = (minute_used + 1, now)
        self.hourly_requests[ip] = (hour_used + 1, now)
        
        return True, remaining_min - 1, remaining_hour - 1
    
    def reset(self, ip: str = None):
        """Reset rate limit for IP"""
        if ip:
            self.minute_requests.pop(ip, None)
            self.hourly_requests.pop(ip, None)
        else:
            self.minute_requests.clear()
            self.hourly_requests.clear()


# Production logger
def get_logger(name: str = None):
    """Get production logger"""
    import logging
    import logging.handlers
    
    config = ProductionConfig()
    
    logger = logging.getLogger(name or config.APP_NAME)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # File handler with rotation
    try:
        handler = logging.handlers.RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
    except Exception:
        handler = logging.StreamHandler()
    
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    logger.addHandler(handler)
    
    return logger


# Health check
def health_check() -> dict:
    """Health check response"""
    return {
        "status": "healthy",
        "service": "web-crawler-agent",
        "version": ProductionConfig.VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


# Error handler
def handle_error(error: Exception, request_id: str = None) -> dict:
    """Handle errors for production"""
    import traceback
    
    logger = get_logger("error")
    logger.error(f"Error {request_id}: {error}\n{traceback.format_exc()}")
    
    error_msg = str(error)
    
    return {
        "error": "Internal server error",
        "request_id": request_id,
        "message": error_msg if "DEBUG" in error_msg else "An error occurred",
    }


# Production initialization
def init_production():
    """Initialize production environment"""
    config = ProductionConfig()
    
    # Disable Streamlit telemetry
    os.environ["STREAMLIT_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # Security settings
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = str(config.ENABLE_CORS).lower()
    os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = str(config.ENABLE_XSRF).lower()
    
    # Validate
    warnings = config.validate()
    if warnings:
        logger = get_logger("init")
        for w in warnings:
            logger.warning(w)
    
    return config


if __name__ == "__main__":
    config = ProductionConfig()
    warnings = config.validate()
    print(f"Config: {config.APP_NAME} v{config.VERSION}")
    print(f"Environment: {config.ENVIRONMENT}")
    if warnings:
        for w in warnings:
            print(w)
    else:
        print("✓ Configuration valid")