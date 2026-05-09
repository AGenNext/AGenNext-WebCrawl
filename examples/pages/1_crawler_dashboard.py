"""Main Crawler Dashboard Page

Web UI for running web crawls with billing integration.
Uses Crawl4AI and Firecrawl tools.
"""
import streamlit as st
import asyncio
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="Web Crawler Dashboard",
    page_icon="🕷️",
    layout="wide",
)

# SEO Meta Tags
st.markdown("""
<head>
    <meta name="description" content="AI-powered web crawling service with Crawl4AI, Firecrawl. Extract content as markdown, JSON, PDF. Single page, depth crawl, sitemap, knowledge graph modes.">
    <meta name="keywords" content="web crawler, web scraping, AI scraping, Crawl4AI, Firecrawl, data extraction, markdown crawler">
    <meta property="og:title" content="AGenNext Web Crawler - AI-Powered Web Crawling">
    <meta property="og:description" content="Powerful web crawling with multiple modes: single page, depth crawl, sitemap, knowledge graph, deep crawl. Uses Crawl4AI & Firecrawl.">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="AGenNext Web Crawler">
    <meta name="twitter:description" content="AI-powered web crawling with Crawl4AI, Firecrawl. Extract content as markdown, JSON, PDF.">
</head>
""", unsafe_allow_html=True)


# ============== TOOL DEFINITIONS ==============
CRAWL4AI_TOOLS = {
    "Basic": {
        "crawl4ai_crawl": "Crawl single URL",
        "crawl4ai_crawl_many": "Crawl multiple URLs",
        "crawl4ai_markdown": "Extract as markdown",
        "crawl4ai_screenshot": "Take screenshot",
        "crawl4ai_pdf": "Generate PDF",
    },
    "Extraction": {
        "crawl4ai_with_css": "Extract with CSS selector",
        "crawl4ai_with_xpath": "Extract with XPath",
        "crawl4ai_with_json": "Extract JSON data",
    },
    "Deep Crawl": {
        "crawl4ai_depth": "Depth-based crawling",
        "crawl4ai_sitemap": "Sitemap extraction",
        "crawl4ai_links": "Extract all links",
    },
    "Advanced": {
        "crawl4ai_js": "Execute JavaScript",
        "crawl4ai_wait": "Wait for elements",
        "crawl4ai_auth": "Handle authentication",
    },
}

FIRECRAWL_TOOLS = {
    "Basic": {
        "firecrawl_scrape": "Scrape URL",
        "firecrawl_crawl": "Crawl website",
        "firecrawl_map": "Sitemap mapping",
    },
    "Extraction": {
        "firecrawl_extract": "Extract structured data",
        "firecrawl_parse": "Parse with schema",
        "firecrawl_search": "Search content",
    },
}

CRAWL_MODES = {
    "single": "Single Page - Crawl one URL",
    "depth": "Depth Crawl - Crawl with depth limit",
    "sitemap": "Sitemap - Parse sitemap.xml",
    "knowledge": "Knowledge Graph - Build entity graph",
    "deep": "Deep Crawl - Crawl all links recursively",
}


# ============== SIDEBAR ==============
with st.sidebar:
    st.header("🕷️ AGenNext Crawler")
    
    # Provider selection
    st.caption("**Provider:**")
    provider = st.radio(
        "Select Provider",
        ["crawl4ai", "firecrawl"],
        format_func=lambda x: {
            "crawl4ai": "🟡 Crawl4AI (Open Source)",
            "firecrawl": "🔥 Firecrawl Cloud",
        }.get(x, x)
    )
    
    # Show tools for selected provider
    st.divider()
    st.caption("**Available Tools:**")
    
    if provider == "crawl4ai":
        for category, tools in CRAWL4AI_TOOLS.items():
            with st.expander(category, expanded=False):
                for tool_name, tool_desc in tools.items():
                    st.caption(f"**{tool_name}**: {tool_desc}")
    else:
        for category, tools in FIRECRAWL_TOOLS.items():
            with st.expander(category, expanded=False):
                for tool_name, tool_desc in tools.items():
                    st.caption(f"**{tool_name}**: {tool_desc}")
    
    # User info
    st.divider()
    st.caption("**Account:** Demo User")
    st.caption("**Plan:** Free")
    st.caption("**Credits:** 100")


# ============== MAIN CONTENT ==============
st.header("🌐 New Crawl")

with st.form("crawl_form"):
    # URL input
    url = st.text_input(
        "Website URL",
        placeholder="https://example.com",
        help="Enter the URL to crawl"
    )
    
    # Mode selection
    col1, col2 = st.columns(2)
    
    with col1:
        mode = st.selectbox(
            "Crawl Mode",
            ["single", "depth", "sitemap", "knowledge", "deep"],
            format_func=lambda x: {
                "single": "Single Page",
                "depth": "Depth Crawl",
                "sitemap": "Sitemap",
                "knowledge": "Knowledge Graph",
                "deep": "Deep Crawl",
            }.get(x, x)
        )
    
    with col2:
        if mode in ["depth", "deep"]:
            max_depth = st.number_input("Max Depth", min_value=1, max_value=10, value=2)
        else:
            max_depth = 1
        
        max_pages = st.slider("Max Pages", 1, 100, 10)
    
    # Submit
    submitted = st.form_submit_button("🚀 Start Crawl", use_container_width=True)


# Process crawl
if submitted and url:
    with st.spinner(f"Crawling {url}..."):
        try:
            # Simulated result for demo
            st.session_state["crawl_url"] = url
            st.session_state["crawl_mode"] = mode
            st.session_state["crawl_status"] = "completed"
            
            st.success(f"✅ Crawl started! Mode: {mode}, Depth: {max_depth}, Max Pages: {max_pages}")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")


# ============== RESULTS ==============
if "crawl_url" in st.session_state:
    st.divider()
    st.header("📄 Results")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📝 Content", "🔗 Links", "📋 Raw JSON"])
    
    with tab1:
        st.success(f"✅ Crawl completed!")
        st.metric("Pages Crawled", st.session_state.get("crawl_pages", 1))
        st.metric("Links Found", st.session_state.get("crawl_links", 0))
        st.metric("Images Found", st.session_state.get("crawl_images", 0))
    
    with tab2:
        st.markdown("### Crawled Content")
        st.info("Crawled content will appear here...")
        
        if st.session_state.get("crawl_status") == "completed":
            st.text_area("Content", value=f"Crawled: {st.session_state.get('crawl_url')}", height=300)
    
    with tab3:
        st.markdown("### Extracted Links")
        st.warning("No links found yet")
    
    with tab4:
        st.markdown("### Raw JSON")
        st.json({
            "url": st.session_state.get("crawl_url", ""),
            "mode": st.session_state.get("crawl_mode", ""),
            "status": st.session_state.get("crawl_status", ""),
            "provider": provider,
        })


# Footer
st.divider()
st.caption("🔵 Version 0.1.0 | Powered by Crawl4AI & Firecrawl")