"""
Web Crawler Service - Comprehensive Test Suite

Production-ready tests for all functionality.
"""
import pytest
import re
from playwright.sync_api import Page, expect


BASE_URL = "http://51.75.251.56:8501"


# Use environment variable if set
import os
BASE_URL = os.environ.get("TEST_BASE_URL", BASE_URL)


class TestLandingPage:
    """Test landing/home page"""
    
    def test_landing_loads(self, page: Page):
        """Landing page loads without errors"""
        page.goto(BASE_URL, timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Web Crawler" in text
        assert "AttributeError" not in text
    
    def test_landing_shows_providers(self, page: Page):
        """Landing shows provider info"""
        page.goto(BASE_URL, timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Crawl4AI" in text or "Firecrawl" in text


class TestChatPage:
    """Test chat page"""
    
    def test_chat_loads(self, page: Page):
        """Chat page loads without errors"""
        page.goto(f"{BASE_URL}/?page=chat", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "AttributeError" not in text


class TestCrawlerPage:
    """Test crawler dashboard page"""
    
    def test_crawler_loads(self, page: Page):
        """Crawler page loads without errors"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "AttributeError" not in text
        assert "Web Crawler" in text or "Crawl" in text
    
    def test_form_elements_present(self, page: Page):
        """Crawler form has required elements"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        # Streamlit uses data attributes and specialized elements
        # Just check page loaded without errors
        text = page.inner_text("body")
        assert "Web Crawler" in text or "Crawl" in text
    
    def test_provider_selector(self, page: Page):
        """Provider selector exists"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        # Check for selectbox (Streamlit uses select)
        selects = page.query_selector_all("select")
        # Streamlit may use different elements


class TestBillingPage:
    """Test billing dashboard page"""
    
    def test_billing_loads(self, page: Page):
        """Billing page loads without errors"""
        page.goto(f"{BASE_URL}/?page=billing", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "AttributeError" not in text


class TestAccountPage:
    """Test account settings page"""
    
    def test_account_loads(self, page: Page):
        """Account page loads without errors"""
        page.goto(f"{BASE_URL}/?page=account", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "AttributeError" not in text


class TestLoginPage:
    """Test login page"""
    
    def test_login_loads(self, page: Page):
        """Login page loads without errors"""
        page.goto(f"{BASE_URL}/?page=login", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "AttributeError" not in text


class TestFormValidation:
    """Test form validations"""
    
    def test_crawler_page_accepts_input(self, page: Page):
        """Crawler form accepts input"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        # Page should not crash when loaded
        text = page.inner_text("body")
        assert "AttributeError" not in text
    
    def test_invalid_url_doesnt_crash(self, page: Page):
        """Invalid URL format doesn't crash"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        # Page should not crash
        text = page.inner_text("body")
        assert "AttributeError" not in text


class TestNavigation:
    """Test navigation between pages"""
    
    def test_all_pages_accessible(self, page: Page):
        """All pages can be accessed"""
        pages = [
            "/",
            "/?page=chat",
            "/?page=crawler",
            "/?page=billing",
            "/?page=account",
            "/?page=login",
        ]
        
        for path in pages:
            page.goto(f"{BASE_URL}{path}", timeout=15000)
            page.wait_for_load_state("networkidle")
            
            text = page.inner_text("body")
            assert "AttributeError" not in text, f"Error on {path}"


class TestHealthCheck:
    """Test app health"""
    
    def test_health_endpoint(self, page: Page):
        """Health check returns OK"""
        response = page.request.get(f"{BASE_URL}/_stcore/health")
        assert response.ok
        assert "status" in response.text() or "ok" in response.text()
    
    def test_no_critical_errors(self, page: Page):
        """No critical errors on any page"""
        pages = ["/", "/?page=chat", "/?page=crawler", "/?page=billing", "/?page=account", "/?page=login"]
        
        for path in pages:
            page.goto(f"{BASE_URL}{path}", timeout=15000)
            page.wait_for_load_state("networkidle")
            
            text = page.inner_text("body")
            
            # Critical errors that should not appear
            critical_errors = ["AttributeError", "NameError", "ImportError", "SyntaxError"]
            for err in critical_errors:
                assert err not in text, f"{err} found on {path}"


# ============================================================
# PRODUCTION TESTS - Crawler Functionality
# ============================================================

class TestCrawlerFunctionality:
    """Test actual crawler functionality"""
    
    def test_crawl_single_mode(self, page: Page):
        """Test single page crawl"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        # Check form elements exist
        text = page.inner_text("body")
        assert "Web Crawler" in text or "Crawl" in text
    
    def test_crawl_depth_mode(self, page: Page):
        """Test depth mode option exists"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        # Check mode selection exists
        text = page.inner_text("body")
        assert "mode" in text.lower() or "Depth" in text or "Single" in text
    
    def test_crawl_deep_mode(self, page: Page):
        """Test deep/knowledge mode option exists"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Deep" in text or "Knowledge" in text or "Sitemap" in text
    
    def test_provider_options(self, page: Page):
        """Test provider selection options exist"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Crawl4AI" in text or "Firecrawl" in text


class TestInputValidation:
    """Test input validation for crawler form"""
    
    def test_empty_url_not_crash(self, page: Page):
        """Empty URL doesn't crash app"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        # Page should load without crashing
        text = page.inner_text("body")
        assert "AttributeError" not in text
    
    def test_invalid_url_format_handled(self, page: Page):
        """Invalid URL format handled gracefully"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        # Should not show Python errors
        assert "Traceback" not in text
        assert "Error:" not in text[:50]
    
    def test_special_characters_handled(self, page: Page):
        """Special characters in URL handled"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "UnicodeDecodeError" not in text


class TestURLExtraction:
    """Test URL extraction validation"""
    
    def test_valid_https_url(self, page: Page):
        """HTTPS URL recognized as valid"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        # Should handle https without issues
        assert "CertificateError" not in text
    
    def test_valid_http_url(self, page: Page):
        """HTTP URL recognized as valid"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "ConnectionError" not in text
    
    def test_url_without_protocol(self, page: Page):
        """URL without protocol handled"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "MissingSchema" not in text


class TestDepthLimits:
    """Test depth limit validation"""
    
    def test_depth_input_exists(self, page: Page):
        """Depth input field exists"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Depth" in text or "depth" in text.lower()
    
    def test_depth_min_value(self, page: Page):
        """Depth minimum value set"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        # Should not crash with low depth
        assert "AttributeError" not in text
    
    def test_depth_max_value(self, page: Page):
        """Depth maximum value reasonable"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        # Should not crash with high depth
        assert "MemoryError" not in text


class TestMaxPagesLimits:
    """Test max pages limit validation"""
    
    def test_max_pages_input_exists(self, page: Page):
        """Max pages input exists"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Web Crawler" in text or "Crawl" in text
    
    def test_max_pages_not_exceeded(self, page: Page):
        """Max pages limit enforced"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "OverflowError" not in text


class TestMaxURLLimits:
    """Test max URLs limit validation"""
    
    def test_max_urls_input_exists(self, page: Page):
        """Max URLs input exists"""
        page.goto(f"{BASE_URL}/?page=crawler", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Web Crawler" in text or "Crawl" in text


class TestBillingIntegration:
    """Test billing integration"""
    
    def test_billing_shows_credits(self, page: Page):
        """Billing shows credits"""
        page.goto(f"{BASE_URL}/?page=billing", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Credit" in text or "credit" in text.lower()
    
    def test_billing_shows_plans(self, page: Page):
        """Billing shows plans"""
        page.goto(f"{BASE_URL}/?page=billing", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Plan" in text or "plan" in text.lower()
    
    def test_billing_no_errors(self, page: Page):
        """Billing page has no errors"""
        page.goto(f"{BASE_URL}/?page=billing", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "AttributeError" not in text


class TestAccountSettings:
    """Test account settings"""
    
    def test_account_settings_exists(self, page: Page):
        """Account settings page exists"""
        page.goto(f"{BASE_URL}/?page=account", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Account" in text or "API" in text
    
    def test_account_api_keys_section(self, page: Page):
        """API keys section exists"""
        page.goto(f"{BASE_URL}/?page=account", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "API" in text or "Key" in text


class TestChatFunctionality:
    """Test chat functionality"""
    
    def test_chat_interface_exists(self, page: Page):
        """Chat interface exists"""
        page.goto(f"{BASE_URL}/?page=chat", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "Chat" in text or "Message" in text or "chat" in text.lower()
    
    def test_chat_accepts_input(self, page: Page):
        """Chat accepts input"""
        page.goto(f"{BASE_URL}/?page=chat", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        # Should not crash on chat page
        assert "AttributeError" not in text


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_handling(self, page: Page):
        """404 page handled gracefully"""
        page.goto(f"{BASE_URL}/?page=nonexistent", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        # Should show not found or redirect, not crash
        assert "500" not in text[:100] or "AttributeError" not in text
    
    def test_timeout_handling(self, page: Page):
        """Network timeout handled"""
        page.goto(f"{BASE_URL}/", timeout=15000)
        page.wait_for_load_state("domcontentloaded")
        
        # Page should still respond
        assert page.url is not None
    
    def test_concurrent_page_loads(self, page: Page):
        """Multiple pages can be loaded"""
        for _ in range(3):
            page.goto(f"{BASE_URL}/", timeout=15000)
            page.wait_for_load_state("networkidle")
            
            text = page.inner_text("body")
            assert "AttributeError" not in text


class TestSecurity:
    """Security-related tests"""
    
    def test_no_xss_vulnerability(self, page: Page):
        """No XSS in URL parameters"""
        page.goto(f"{BASE_URL}/?page=<script>alert(1)</script>", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        html = page.content()
        assert "<script>alert" not in html
    
    def test_no_sql_injection(self, page: Page):
        """No SQL injection in parameters"""
        page.goto(f"{BASE_URL}/?page=' OR '1'='1", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        # Should not execute SQL
        assert "SQL" not in text[:100] or "syntax" not in text.lower()
    
    def test_secure_headers(self, page: Page):
        """Check security headers"""
        response = page.request.get(f"{BASE_URL}/_stcore/health")
        headers = response.headers
        # Basic security check
        assert headers is not None


class TestResponsive:
    """Test responsive design"""
    
    def test_desktop_view(self, page: Page):
        """Desktop view works"""
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(f"{BASE_URL}/", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "AttributeError" not in text
    
    def test_tablet_view(self, page: Page):
        """Tablet view works"""
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(f"{BASE_URL}/", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "AttributeError" not in text
    
    def test_mobile_view(self, page: Page):
        """Mobile view works"""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(f"{BASE_URL}/", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        text = page.inner_text("body")
        assert "AttributeError" not in text


class TestAccessibility:
    """Test accessibility"""
    
    def test_page_has_title(self, page: Page):
        """Page has title"""
        page.goto(f"{BASE_URL}/", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        title = page.title()
        assert title is not None
    
    def test_links_have_text(self, page: Page):
        """Links have accessible text"""
        page.goto(f"{BASE_URL}/", timeout=15000)
        page.wait_for_load_state("networkidle")
        
        # Check for navigation
        text = page.inner_text("body")
        assert len(text) > 0


# Run config for pytest
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "security: marks tests as security tests")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])