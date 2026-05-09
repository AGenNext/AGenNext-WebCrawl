"""Main Crawler Dashboard Page

Web UI for running web crawls with billing integration.
"""
import streamlit as st
import asyncio
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Web Crawler Dashboard",
    page_icon="🕷️",
    layout="wide",
)


st.title("🕷️ Web Crawler Dashboard")
st.markdown("Crawl websites with AI-powered extraction")


# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Provider selection
    provider = st.selectbox(
        "Crawler Provider",
        ["crawl4ai", "firecrawl", "firecrawl-opensource"],
        format_func=lambda x: {
            "crawl4ai": "Crawl4AI (Free)",
            "firecrawl": "Firecrawl Cloud",
            "firecrawl-opensource": "Firecrawl OS",
        }.get(x, x)
    )
    
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
        depth = st.number_input("Depth", min_value=1, max_value=10, value=2)
    
    # Options
    with st.expander("Advanced Options"):
        max_pages = st.slider("Max Pages", 1, 100, 10)
        max_urls = st.slider("Max URLs", 10, 1000, 100)
    
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