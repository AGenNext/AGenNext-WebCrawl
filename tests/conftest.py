"""
Playwright configuration for pytest
"""
import pytest


@pytest.fixture(scope="session")
def browser():
    """Launch browser for tests"""
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    yield browser
    browser.close()
    pw.stop()


@pytest.fixture(scope="function")
def page(browser):
    """Create new page for each test"""
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    yield page
    page.close()