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
        "crawl4ai_with_regex": "Extract with Regex",
        "crawl4ai_with_llm": "Extract with LLM schema",
    },
    "Deep Crawl": {
        "crawl4ai_deep_bfs": "BFS deep crawl",
        "crawl4ai_deep_dfs": "DFS deep crawl",
    },
    "Advanced": {
        "crawl4ai_stealth": "Stealth browsing",
        "crawl4ai_js_render": "JavaScript rendering",
        "crawl4ai_with_proxy": "Crawl with proxy",
    },
}

FIRECRAWL_TOOLS = {
    "Basic": {
        "firecrawl_crawl": "Crawl single URL",
        "firecrawl_crawl_urls": "Crawl multiple URLs",
        "firecrawl_scrape": "Scrape to markdown",
        "firecrawl_search": "Web search",
    },
    "Parse": {
        "firecrawl_sitemap": "Parse sitemap",
        "firecrawl_extract": "Extract with schema",
    },
    "Special": {
        "firecrawl_youtube": "YouTube to markdown",
        "firecrawl_github": "GitHub to markdown",
        "firecrawl_pdf": "PDF to markdown",
    },
}

# Crawl modes
CRAWL_MODES = {
    "single": "Single Page - Crawl one URL only",
    "depth": "Depth Crawl - Crawl with depth limit",
    "sitemap": "Sitemap - Parse sitemap.xml",
    "knowledge": "Knowledge Graph - Build knowledge from content",
    "deep": "Deep Crawl - Crawl all links recursively",
}


st.title("🕷️ Web Crawler Dashboard")
st.markdown("AI-Powered Web Crawling with Crawl4AI & Firecrawl")


# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Provider selection
    provider = st.selectbox(
        "Crawler Provider",
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


# Main content
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
            list(CRAWL_MODES.keys()),
            format_func=lambda x: CRAWL_MODES[x].split(" - ")[0]
        )
    
    with col2:
        if mode in ["depth", "deep"]:
            max_depth = st.number_input("Max Depth", min_value=1, max_value=10, value=2)
        else:
            max_depth = 1
    
    # Tool selection
    if provider == "crawl4ai":
        tool_category = st.selectbox(
            "Tool Category",
            list(CRAWL4AI_TOOLS.keys())
        )
        selected_tool = st.selectbox(
            "Select Tool",
            list(CRAWL4AI_TOOLS[tool_category].keys()),
            format_func=lambda x: CRAWL4AI_TOOLS[tool_category][x]
        )
    else:
        tool_category = st.selectbox(
            "Tool Category",
            list(FIRECRAWL_TOOLS.keys())
        )
        selected_tool = st.selectbox(
            "Select Tool",
            list(FIRECRAWL_TOOLS[tool_category].keys()),
            format_func=lambda x: FIRECRAWL_TOOLS[tool_category][x]
        )
    
    # Options
    with st.expander("⚙️ Advanced Options"):
        col3, col4 = st.columns(2)
        with col3:
            js_render = st.checkbox("JavaScript Rendering", value=False)
            wait_for = st.text_input("Wait For Selector", placeholder=".content")
        with col4:
            stealth = st.checkbox("Stealth Mode", value=False)
            timeout = st.number_input("Timeout (sec)", min_value=10, value=30)
    
    # Submit
    submitted = st.form_submit_button("🚀 Start Crawl", type="primary")
    
    if submitted and url:
        st.session_state.crawl_url = url
        st.session_state.crawl_mode = mode
        st.session_state.crawl_tool = selected_tool
        st.session_state.crawl_provider = provider


# Results section
if "crawl_url" in st.session_state:
    st.divider()
    st.header("📊 Results")
    
    # Status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("URL", st.session_state.crawl_url[:30] + "...")
    with col2:
        st.metric("Mode", st.session_state.crawl_mode)
    with col3:
        st.metric("Tool", st.session_state.crawl_tool)
    
    # Result display tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Markdown", "🔗 Links", "🖼️ Images", "📋 Raw"])
    
    with tab1:
        st.markdown("### Crawled Content")
        st.info("🔄 Run crawl to see content here...")
        st.markdown("""
        **Note:** Install dependencies to enable:
        ```bash
        pip install crawl4ai firecrawl
        ```
        """)
    
    with tab2:
        st.markdown("### Extracted Links")
        st.info("Links will appear here after crawl")
    
    with tab3:
        st.markdown("### Extracted Images")
        st.info("Images will appear here after crawl")
    
    with tab4:
        st.markdown("### Raw JSON")
        st.json({
            "url": st.session_state.get("crawl_url", ""),
            "mode": st.session_state.get("crawl_mode", ""),
            "tool": st.session_state.get("crawl_tool", ""),
            "provider": st.session_state.get("crawl_provider", ""),
        })


# Footer
st.divider()
st.caption(f"🔵 Version 0.1.0 | Powered by Crawl4AI & Firecrawl")
    
    # Submit
    submitted = st.form_submit_button("🚀 Start Crawl", use_container_width=True)


# Process crawl
if submitted and url:
    with st.spinner(f"Crawling {url}..."):
        try:
            from crawler_agent import CrawlAgent
            
            # Create agent
            agent = CrawlAgent(provider=provider)
            
            # Run crawl
            result = asyncio.run(agent.crawl(url, mode=mode, depth=depth, max_pages=max_pages))
            
            # Show results
            st.success(f"✅ Crawl completed! {result.get('total_pages', 0)} pages")
            
            # Display results
            st.divider()
            st.header("📄 Results")
            
            if result.get("crawled_pages"):
                for i, page in enumerate(result["crawled_pages"]):
                    with st.expander(f"📄 {page['url']}"):
                        st.caption(f"**URL:** {page['url']}")
                        st.caption(f"**Links:** {len(page.get('links', []))}")
                        
                        # Show markdown preview
                        md = page.get("markdown", "")
                        if md:
                            st.text(md[:500] + "..." if len(md) > 500 else md)
                        
                        # Show links
                        links = page.get("links", [])
                        if links:
                            st.write(f"**Found {len(links)} links:**")
                            for link in links[:10]:
                                st.code(link)
            
            # Knowledge graph
            if result.get("knowledge_graph") and mode == "knowledge":
                st.divider()
                st.header("🔗 Knowledge Graph")
                
                kg = result["knowledge_graph"]
                st.write(f"**Entities:** {len(kg.get('entities', []))}")
                st.write(f"**Relationships:** {len(kg.get('relationships', []))}")
                
                for entity in kg.get("entities", [])[:10]:
                    st.write(f"- {entity.get('type')}: {entity.get('value')}")
            
            # Raw result
            with st.expander("View Raw JSON"):
                st.json(result)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")


# Recent crawls (placeholder)
st.divider()
st.header("📝 Recent Crawls")

recent = [
    {"date": "2024-01-15", "url": "example.com", "mode": "depth", "pages": 3},
    {"date": "2024-01-14", "url": "httpbin.org", "mode": "single", "pages": 1},
]

for crawl in recent:
    st.write(f"🕷️ {crawl['date']} - {crawl['url']} ({crawl['mode']}, {crawl['pages']} pages)")


# Help
with st.sidebar.expander("❓ Help"):
    st.markdown("""
    **Crawl Modes:**
    - **Single:** Crawl one URL
    - **Depth:** Crawl with depth limit
    - **Knowledge:** Extract knowledge graph
    - **Deep:** Crawl all links
    """)


if __name__ == "__main__":
    st.run()