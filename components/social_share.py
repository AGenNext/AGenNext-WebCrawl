"""
Social Share Component

Add social media sharing links to pages.
"""
import streamlit as st


def get_share_url(platform: str, url: str, title: str = None) -> str:
    """Get share URL for platform."""
    import urllib.parse
    
    base_urls = {
        "twitter": "https://twitter.com/intent/tweet",
        "facebook": "https://www.facebook.com/sharer/sharer.php",
        "linkedin": "https://www.linkedin.com/shareArticle",
        "reddit": "https://reddit.com/submit",
        "copy": None,  # Handled specially
    }
    
    if title:
        text = f"{title} - {url}"
    else:
        text = url
    
    if platform == "twitter":
        return f"{base_urls['twitter']}?text={urllib.parse.quote(text)}"
    elif platform == "facebook":
        return f"{base_urls['facebook']}?u={urllib.parse.quote(url)}"
    elif platform == "linkedin":
        return f"{base_urls['linkedin']}?url={urllib.parse.quote(url)}"
    elif platform == "reddit":
        return f"{base_urls['reddit']}?url={urllib.parse.quote(url)}"
    
    return url


def add_social_share(
    title: str = "Web Crawler Service",
    url: str = "https://webcrawl.agnxxt.com",
):
    """
    Add social share buttons to the page.
    
    Args:
        title: Content title
        url: Content URL to share
    """
    import urllib.parse
    
    # Share URLs
    share_text = urllib.parse.quote(f"Check out {title}:")
    share_urls = {
        "twitter": f"https://twitter.com/intent/tweet?text={share_text}&url={urllib.parse.quote(url)}",
        "facebook": f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(url)}",
        "linkedin": f"https://www.linkedin.com/shareArticle?mini=true&url={urllib.parse.quote(url)}",
        "reddit": f"https://reddit.com/submit?url={urllib.parse.quote(url)}",
    }
    
    # Icons (use emoji for simplicity)
    icons = {
        "twitter": "𝕏",
        "facebook": "📘",
        "linkedin": "💼",
        "reddit": "🔴",
    }
    
    # HTML for share buttons
    html = f"""
    <style>
    .social-share {{ display: flex; gap: 10px; margin: 20px 0; }}
    .social-btn {{
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        border-radius: 20px;
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
    }}
    .social-btn.twitter {{ background: #1DA1F2; color: white; }}
    .social-btn.facebook {{ background: #4267B2; color: white; }}
    .social-btn.linkedin {{ background: #0077b5; color: white; }}
    .social-btn.reddit {{ background: #FF4500; color: white; }}
    </style>
    
    <div class="social-share">
        <a class="social-btn twitter" href="{share_urls['twitter']}" target="_blank">
            {icons['twitter']} Twitter
        </a>
        <a class="social-btn facebook" href="{share_urls['facebook']}" target="_blank">
            {icons['facebook']} Facebook
        </a>
        <a class="social-btn linkedin" href="{share_urls['linkedin']}" target="_blank">
            {icons['linkedin']} LinkedIn
        </a>
        <a class="social-btn reddit" href="{share_urls['reddit']}" target="_blank">
            {icons['reddit']} Reddit
        </a>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
    
    # Copy link button
    col = st.columns(5)
    with col[0]:
        if st.button("📋 Copy Link", key="copy_link"):
            st.write(f"URL: {url}")


# Default social links
SOCIAL_LINKS = {
    "twitter": "https://twitter.com/agnxxt",
    "github": "https://github.com/AGenNext/AGenNext-WebCrawl",
    "discord": "https://discord.gg/agnxxt",
}


def add_footer_social():
    """Add social links to footer."""
    html = """
    <style>
    .footer-social { display: flex; gap: 15px; margin-top: 20px; }
    .footer-social a { 
        color: #666; 
        text-decoration: none;
        font-size: 24px;
    }
    </style>
    
    <div class="footer-social">
        <a href="https://twitter.com/agnxxt" target="_blank" title="Twitter">𝕏</a>
        <a href="https://github.com/AGenNext/AGenNext-WebCrawl" target="_blank" title="GitHub">🐙</a>
        <a href="https://discord.gg/agnxxt" target="_blank" title="Discord">💬</a>
        <a href="https://github.com/AGenNext/AGenNext-WebCrawl" target="_blank" title="Star us on GitHub">⭐</a>
    </div>
    
    <div style="margin-top: 10px;">
        <a href="https://github.com/AGenNext/AGenNext-WebCrawl" target="_blank" 
           style="background: #24292f; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 14px;">
            ⭐ Star us on GitHub
        </a>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


# GitHub star link
GITHUB_URL = "https://github.com/AGenNext/AGenNext-WebCrawl"
GITHUB_STAR_URL = f"{GITHUB_URL}/stargazers"


def add_github_star_button():
    """Add GitHub star button."""
    html = f"""
    <a href="{GITHUB_URL}" target="_blank" 
       style="display: inline-flex; align-items: center; gap: 8px;
              background: #24292f; color: white; padding: 10px 20px;
              border-radius: 6px; text-decoration: none; font-size: 16px;
              font-weight: 600;">
        ⭐ Star on GitHub
    </a>
    """
    st.markdown(html, unsafe_allow_html=True)


if __name__ == "__main__":
    st.title("Social Share Test")
    add_social_share()
    st.write("Check below for share buttons!")