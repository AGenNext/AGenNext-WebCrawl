"""
How-to Guide - Web Crawler Service

Documentation and guides for using the application.
"""
import streamlit as st
import sys
sys.path.insert(0, '/workspace/project')
from version import __version__, APP_TITLE


def main():
    st.set_page_config(
        page_title=f"How-to Guide - {APP_TITLE}",
        page_icon="📖",
        layout="wide",
    )
    
    st.title("📖 How-to Guide")
    st.markdown(f"**Version:** {__version__}")
    
    st.divider()
    
    # Navigation
    st.subheader("🧭 Quick Navigation")
    st.markdown("""
    - [Getting Started](#getting-started)
    - [Quick Start](#quick-start)
    - [Crawl Modes](#crawl-modes)
    - [Providers](#providers)
    - [API Reference](#api-reference)
    - [Troubleshooting](#troubleshooting)
    """)
    
    st.divider()
    
    # Getting Started
    st.header("🚀 Getting Started")
    
    st.subheader("Prerequisites")
    st.markdown("""
    - Python 3.10+
    - Docker (for containerized deployment)
    - API keys for supported providers
    """)
    
    st.subheader("Installation")
    st.code("""# Clone the repository
git clone https://github.com/AGenNext/AGenNext-WebCrawl.git
cd AGenNext-WebCrawl

# Install dependencies
pip install -r requirements.txt

# Or use Docker
docker-compose up -d
""", language="bash")
    
    st.divider()
    
    # Quick Start
    st.header("⚡ Quick Start")
    
    st.subheader("Python SDK")
    st.code("""from crawler_agent import CrawlAgent

agent = CrawlAgent(provider="crawl4ai")
result = await agent.crawl(
    "https://example.com",
    mode="depth",
    depth=2
)
print(result)
""", language="python")
    
    st.subheader("REST API")
    st.code("""curl -X POST https://api.example.com/crawl \\
  -H "Authorization: Bearer YOUR_KEY" \\
  -d '{"url": "https://example.com"}'
""", language="bash")
    
    st.subheader("Web Interface")
    st.markdown("""
    1. Navigate to http://51.75.251.56:8501
    2. Go to Crawler page
    3. Enter URL to crawl
    4. Select mode and options
    5. Click "Start Crawl"
    """)
    
    st.divider()
    
    # Crawl Modes
    st.header("🕷️ Crawl Modes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Single Mode")
        st.markdown("""
        Crawls a single URL.
        
        **Use case:** Quick page fetch
        
        Parameters:
        - `url` (required)
        """)
        
        st.subheader("Depth Mode")
        st.markdown("""
        Crawls pages up to N levels deep.
        
        **Use case:** Site exploration
        
        Parameters:
        - `url` (required)
        - `depth` (1-10)
        - `max_pages` (1-100)
        """)
    
    with col2:
        st.subheader("Deep Mode")
        st.markdown("""
        Crawls all links recursively.
        
        **Use case:** Complete site crawl
        
        Parameters:
        - `url` (required)
        - `max_pages` (1-1000)
        - `max_urls` (10-10000)
        """)
        
        st.subheader("Sitemap Mode")
        st.markdown("""
        Parses sitemap.xml.
        
        **Use case:** Find all pages
        
        Parameters:
        - `url` (required)
        """)
    
    st.divider()
    
    # Providers
    st.header("☁️ Providers")
    
    st.markdown("""
    | Provider | API Key | Features |
    |----------|--------|-----------|
    | Crawl4AI | Self-hosted or API | Fast, free tier |
    | Firecrawl | api.firecrawl.dev | AI-powered |
    
    ### Setting API Keys
    1. Go to Account page
    2. Enter your API key
    3. Save
    """)
    
    st.divider()
    
    # API Reference
    st.header("📚 API Reference")
    
    st.subheader("Python SDK")
    st.code("""from crawler_agent import CrawlAgent

# Initialize
agent = CrawlAgent(
    provider="crawl4ai",
    api_key="your-key"
)

# Single crawl
result = await agent.crawl(url="https://example.com")

# With options
result = await agent.crawl(
    url="https://example.com",
    mode="depth",
    depth=2,
    max_pages=50
)

# Check status
print(result.status)
print(result.content)
""", language="python")
    
    st.subheader("REST Endpoints")
    st.markdown("""
    | Method | Endpoint | Description |
    |--------|----------|-------------|
    | POST | /crawl | Start a crawl |
    | GET | /status/{id} | Get crawl status |
    | GET | /result/{id} | Get crawl result |
    | DELETE | /crawl/{id} | Cancel crawl |
    """)
    
    st.divider()
    
    # Troubleshooting
    st.header("🔧 Troubleshooting")
    
    st.markdown("""
    ### Common Issues
    
    **Q: Crawl fails with timeout**
    - A: Increase timeout in settings
    
    **Q: API key not accepted**
    - A: Check key is valid for provider
    
    **Q: Too many pages**
    - A: Reduce max_pages limit
    
    **Q: Rate limit exceeded**
    - A: Wait and retry, or upgrade plan
    
    ### Get Help
    - [GitHub Issues](https://github.com/AGenNext/AGenNext-WebCrawl/issues)
    - [Discord](https://discord.gg/agnxxt)
    """)


if __name__ == "__main__":
    main()