"""
Changelog Page - Web Crawler Service

Shows the changelog/roadmap for the application.
"""
import streamlit as st
import sys
sys.path.insert(0, '/workspace/project')
from version import __version__, APP_TITLE


def main():
    st.set_page_config(
        page_title=f"Changelog - {APP_TITLE}",
        page_icon="📋",
        layout="wide",
    )
    
    st.title("📋 Changelog")
    st.markdown(f"**Current Version:** {__version__}")
    
    st.divider()
    
    # Version 0.1.0
    st.subheader("🎉 Version 0.1.0 - 2026-05-09")
    
    st.markdown("### Added")
    st.markdown("""
    - Web Crawler Service multi-page Streamlit app
    - Landing page with provider info
    - Chat page for conversational crawling
    - Crawler dashboard with form inputs
    - Billing dashboard with credits/plans
    - Account settings with API keys
    - Login page
    - Crawl modes: Single, Depth, Deep/Knowledge, Sitemap
    - Provider support: Crawl4AI, Firecrawl
    - Depth and max pages/URLs limits
    - Test suite with Playwright (48 tests)
    - CI/CD pipeline for testing
    - Docker Compose deployment
    """)
    
    st.markdown("### Fixed")
    st.markdown("""
    - st.run() error in app.py
    - Removed broken Traefik labels
    - Updated Docker Compose version to 3.9
    """)
    
    st.markdown("### Security")
    st.markdown("""
    - XSS protection tests
    - SQL injection protection tests
    """)
    
    st.divider()
    
    # Roadmap
    st.subheader("🗺️ Roadmap")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Upcoming Features")
        st.markdown("""
        - [ ] REST API endpoints
        - [ ] User authentication
        - [ ] Credit system integration
        - [ ] Billing/payment integration
        - [ ] More provider support
        - [ ] Crawl history
        - [ ] Export results (PDF, JSON, CSV)
        - [ ] Scheduled crawls
        - [ ] Webhook integration
        """)
    
    with col2:
        st.markdown("#### Future Plans")
        st.markdown("""
        - [ ] Multi-user support
        - [ ] Team collaboration
        - [ ] Custom crawlers
        - [ ] Browser extension
        - [ ] API rate limiting
        - [ ] Usage analytics
        - [ ] SSO integration
        - [ ] Custom domains
        """)
    
    st.divider()
    
    # Links
    st.subheader("🔗 Links")
    st.markdown("""
    - [GitHub Repository](https://github.com/AGenNext/AGenNext-WebCrawl)
    - [Report Issues](https://github.com/AGenNext/AGenNext-WebCrawl/issues)
    - [API Documentation](https://github.com/AGenNext/AGenNext-WebCrawl#api)
    """)


if __name__ == "__main__":
    main()