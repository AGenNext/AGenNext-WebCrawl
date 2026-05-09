"""
SEO Meta Tags Component

Adds Open Graph and Twitter Card meta tags to Streamlit pages.
"""
import streamlit as st


def add_seo_meta(
    title: str,
    description: str,
    url: str = None,
    image: str = None,
    site_name: str = "Web Crawler Service",
    twitter_card: str = "summary_large_image",
):
    """
    Add SEO meta tags to the page.
    """
    meta_tags = f"""
    <meta name="description" content="{description}">
    <meta name="author" content="AGenNext Team">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{site_name}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    """
    
    if url:
        meta_tags += f'<meta property="og:url" content="{url}">\n'
    
    if image:
        meta_tags += f'<meta property="og:image" content="{image}">\n'
    
    # Twitter
    meta_tags += f"""
    <!-- Twitter -->
    <meta property="twitter:card" content="{twitter_card}">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{description}">
    """
    
    if image:
        meta_tags += f'<meta property="twitter:image" content="{image}">\n'
    
    st.markdown(meta_tags, unsafe_allow_html=True)


def get_seo_config(
    title: str,
    page_icon: str = "🕷️",
) -> dict:
    """Get SEO config for st.set_page_config."""
    return {
        "page_title": f"{title} - Web Crawler Service",
        "page_icon": page_icon,
    }


# Default SEO values
DEFAULT_TITLE = "Web Crawler Service"
DEFAULT_DESCRIPTION = "AI-powered web crawling with multiple providers (Crawl4AI, Firecrawl). Multi-mode crawling: Single, Depth, Deep, Sitemap, Knowledge Graph."
DEFAULT_URL = "https://webcrawl.agnxxt.com"
DEFAULT_IMAGE = "https://webcrawl.agnxxt.com/og-image.png"


if __name__ == "__main__":
    st.set_page_config(**get_seo_config("Test"))
    add_seo_meta("Test", "Test description")
    st.title("SEO Test")