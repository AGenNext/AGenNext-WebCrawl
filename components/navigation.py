"""Standardized Navigation Component"""
import streamlit as st


# Navigation pages config
NAV_PAGES = [
    {"path": "landing.py", "icon": "🏠", "label": "Landing", "section": "main"},
    {"path": "0_chat.py", "icon": "💬", "label": "Chat", "section": "main"},
    {"path": "1_crawler_dashboard.py", "icon": "🌐", "label": "Crawler", "section": "main"},
    {"path": "2_billing_dashboard.py", "icon": "💳", "label": "Billing", "section": "account"},
    {"path": "3_account_settings.py", "icon": "👤", "label": "Account", "section": "account"},
    {"path": "4_login.py", "icon": "🔐", "label": "Login", "section": "account"},
    {"path": "5_changelog.py", "icon": "📋", "label": "Changelog", "section": "docs"},
    {"path": "6_howto.py", "icon": "📖", "label": "How-to", "section": "docs"},
    {"path": "7_pricing.py", "icon": "💰", "label": "Pricing", "section": "docs"},
    {"path": "8_faq.py", "icon": "❓", "label": "FAQ", "section": "docs"},
]


def render_navigation():
    """Render standardized navigation sidebar"""
    
    with st.sidebar:
        st.title("🕷️ Web Crawler")
        st.caption("AI-Powered Web Crawling")
        
        st.divider()
        
        # Group pages by section
        sections = {
            "main": [p for p in NAV_PAGES if p["section"] == "main"],
            "account": [p for p in NAV_PAGES if p["section"] == "account"],
            "docs": [p for p in NAV_PAGES if p["section"] == "docs"],
        }
        
        # Main section
        with st.expander("📌 Main", expanded=True):
            for page in sections.get("main", []):
                st.page_link(
                    f"pages/{page['path']}",
                    label=f"{page['icon']} {page['label']}"
                )
        
        # Account section
        with st.expander("👤 Account", expanded=False):
            for page in sections.get("account", []):
                st.page_link(
                    f"pages/{page['path']}",
                    label=f"{page['icon']} {page['label']}"
                )
        
        # Docs section
        with st.expander("📚 Docs", expanded=False):
            for page in sections.get("docs", []):
                st.page_link(
                    f"pages/{page['path']}",
                    label=f"{page['icon']} {page['label']}"
                )
        
        st.divider()
        
        # User info
        if st.session_state.get("authenticated"):
            user = st.session_state.get("user", {})
            st.caption(f"**{user.get('name', 'User')}**")
            st.caption(f"Plan: {user.get('plan', 'free').title()}")
            st.caption(f"Credits: {user.get('credits', 0)}")
            
            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
        else:
            st.caption("Not logged in")
            st.page_link("pages/4_login.py", label="Login", use_container_width=True)