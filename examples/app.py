"""
Web Crawler Service - Multi-Page App

Run this file to start all pages:
    streamlit run examples/app.py

Then navigate to:
    http://localhost:8501
"""
import streamlit as st
from datetime import datetime
import sys
sys.path.insert(0, '/workspace/project')
from version import __version__, APP_NAME, APP_TITLE
from components.seo_meta import add_seo_meta, get_seo_config, DEFAULT_DESCRIPTION

# Page config with SEO
seo_config = get_seo_config(APP_TITLE)
st.set_page_config(
    page_title=seo_config["page_title"],
    page_icon=seo_config["page_icon"],
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add SEO meta
add_seo_meta(APP_TITLE, DEFAULT_DESCRIPTION)


# Session state for auth
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = {
        "email": "demo@user.com",
        "name": "Demo User",
        "plan": "free",
        "credits": 100,
    }


def login(email: str, password: str) -> bool:
    """Simple login (use real auth in production)"""
    return email == "demo@user.com" and password == "demo123"


# Sidebar - Navigation
with st.sidebar:
    st.title("🕷️ Web Crawler")
    st.caption("AI-Powered Web Crawling")
    
    st.divider()
    
    # Navigation
    st.page_link("pages/landing.py", label="🏠 Landing")
    st.page_link("pages/0_chat.py", label="💬 Chat")
    st.page_link("pages/1_crawler_dashboard.py", label="🌐 Crawler")
    st.page_link("pages/2_billing_dashboard.py", label="💳 Billing")
    st.page_link("pages/3_account_settings.py", label="👤 Account")
    st.page_link("pages/4_login.py", label="🔐 Login")
    st.page_link("pages/5_changelog.py", label="📋 Changelog")
    st.page_link("pages/6_howto.py", label="📖 How-to")
    st.page_link("pages/7_pricing.py", label="💰 Pricing")
    st.page_link("pages/8_faq.py", label="❓ FAQ")
    
    st.divider()
    
    # User info (if logged in)
    if st.session_state.authenticated:
        user = st.session_state.user
        st.caption(f"**{user['name']}**")
        st.caption(f"Plan: {user['plan'].title()}")
        st.caption(f"Credits: {user['credits']}")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()
    else:
        st.caption("Not logged in")


# Main page
st.title("🕷️ Welcome to Web Crawler Service")
st.markdown("""
AI-powered web crawling with multiple providers and billing.
""")

# Features
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Providers", "3")
    st.caption("Crawl4AI, Firecrawl")

with col2:
    st.metric("Crawl Modes", "5")
    st.caption("Single, Depth, Deep...")

with col3:
    st.metric("Billing", "3 Ways")
    st.caption("Credits, Plans, Usage")

with col4:
    st.metric("API", "Yes")
    st.caption("REST API + Python SDK")

# Quick start
st.divider()
st.header("🚀 Quick Start")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Python SDK")
    st.code("""
from crawler_agent import CrawlAgent

agent = CrawlAgent(provider="crawl4ai")
result = await agent.crawl(
    "https://example.com",
    mode="depth",
    depth=2
)
    """, language="python")

with col2:
    st.markdown("### REST API")
    st.code("""
curl -X POST https://api.example.com/crawl \\
  -H "Authorization: Bearer YOUR_KEY" \\
  -d '{"url": "https://example.com"}'
    """)

# Links
st.divider()
st.markdown("""
- **[Crawler Dashboard](pages/1_crawler_dashboard.py)** - Run crawls
- **[Billing](pages/2_billing_dashboard.py)** - Manage credits & plans
- **[Account](pages/3_account_settings.py)** - Settings & API keys
- **[Login](pages/4_login.py)** - Sign in
""")

# Footer
st.divider()
st.caption(f"{APP_TITLE} v{__version__} • {datetime.now().year}")


if __name__ == "__main__":
    import sys
    sys.exit(0)  # Streamlit runs via CLI: streamlit run examples/app.py