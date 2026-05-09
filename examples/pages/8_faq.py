"""
FAQ Page - Web Crawler Service

Frequently asked questions.
"""
import streamlit as st
import sys
sys.path.insert(0, '/workspace/project')
from version import __version__, APP_TITLE
from components.seo_meta import add_seo_meta, get_seo_config, DEFAULT_DESCRIPTION
from components.social_share import add_social_share


def main():
    # SEO
    seo = get_seo_config("FAQ")
    st.set_page_config(
        page_title=seo["page_title"],
        page_icon="❓",
        layout="wide",
    )
    add_seo_meta("FAQ", "Frequently Asked Questions about Web Crawler Service")
    
    st.title("❓ Frequently Asked Questions")
    st.markdown("Findanswers to common questions below")
    
    st.divider()
    
    # General
    st.header("💬 General Questions")
    
    with st.expander("What is Web Crawler Service?"):
        st.markdown("""
        Web Crawler Service is an AI-powered web crawling platform that 
        uses advanced crawlers like **Crawl4AI** and **Firecrawl** to extract 
        content from websites. It's built with LangGraph SDK for robust workflows.
        """)
    
    with st.expander("What programming languages are supported?"):
        st.markdown("""
        The service supports **Python** via our SDK and any language 
        that can make HTTP requests via our REST API.
        """)
    
    with st.expander("Is it free to use?"):
        st.markdown("""
        We offer a **Free plan** with 100 pages/month. Paid plans start 
        at $29/month for 10,000 pages. See our [Pricing](pages/7_pricing.py) 
        for details.
        """)
    
    st.divider()
    
    # Technical
    st.header("🔧 Technical Questions")
    
    with st.expander("How do I get an API key?"):
        st.markdown("""
        1. Go to the **Account** page
        2. Navigate to API Keys section
        3. Click "Generate New Key"
        4. Copy and save your key securely
        """)
    
    with st.expander("What crawl modes are available?"):
        st.markdown("""
        | Mode | Description |
        |------|-------------|
        | **Single** | Crawl one URL |
        | **Depth** | Crawl N levels deep |
        | **Deep** | Crawl all links recursively |
        | **Sitemap** | Parse sitemap.xml |
        | **Knowledge** | Extract structured knowledge |
        """)
    
    with st.expander("What providers are supported?"):
        st.markdown("""
        - **Crawl4AI** - Fast, open-source crawler
        - **Firecrawl** - AI-powered crawling
        """)
    
    with st.expander("How long does a crawl take?"):
        st.markdown("""
        Crawl time depends on:
        - Number of pages
        - Website response time
        - Depth setting
        - Server load
        
        Typical crawl: ~1-5 pages/second
        """)
    
    st.divider()
    
    # Billing
    st.header("💰 Billing Questions")
    
    with st.expander("How do credits work?"):
        st.markdown("""
        Each page crawled costs **1 credit**. Deep crawl mode 
        uses more credits based on pages crawled. Unused credits 
        roll over to next month.
        """)
    
    with st.expander("Can I get a refund?"):
        st.markdown("""
        Yes! We offer a **30-day money-back guarantee** for all 
        paid plans.
        """)
    
    with st.expander("How do I cancel my subscription?"):
        st.markdown("""
        Go to **Account** > **Billing** > **Cancel Subscription**.
        Your plan continues until the end of billing period.
        """)
    
    st.divider()
    
    # Troubleshooting
    st.header("🔍 Troubleshooting")
    
    with st.expander("Crawl failed - What now?"):
        st.markdown("""
        Common causes:
        - **Rate limited** - Wait and retry
        - **Invalid URL** - Check URL format
        - **Timeout** - Increase timeout setting
        - **Blocked** - Use different provider
        
        Check logs for specific error messages.
        """)
    
    with st.expander("Getting 403/429 errors?"):
        st.markdown("""
        - **403** = Forbidden. The site blocks crawlers.
        - **429** = Too many requests. Wait and retry.
        
        Try using a different provider or reducing crawl speed.
        """)
    
    with st.expander("Slow crawl performance?"):
        st.markdown("""
        To speed up crawls:
        - Use more parallel connections
        - Reduce depth
        - Use single mode instead of deep
        - Upgrade to Pro plan
        """)
    
    st.divider()
    
    # Contact
    st.header("📞 Need More Help?")
    st.markdown("""
    - **Email**: support@agnxxt.com
    - **Discord**: [Join our community](https://discord.gg/agnxxt)
    - **GitHub**: [Open an issue](https://github.com/AGenNext/AGenNext-WebCrawl/issues)
    """)


if __name__ == "__main__":
    main()