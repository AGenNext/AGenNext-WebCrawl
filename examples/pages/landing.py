"""
Landing Page for Web Crawler Service

SEO-optimized landing page with metadata, features, and pricing.
"""
import streamlit as st
from datetime import datetime

# Page config with SEO metadata
st.set_page_config(
    page_title="Web Crawler Agent - AI-Powered Web Crawling Service",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for landing page
st.markdown("""
<style>
    /* Hero section */
    .Hero {
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        margin-bottom: 40px;
    }
    
    /* Feature cards */
    .FeatureCard {
        padding: 30px;
        background: #0f0f23;
        border-radius: 15px;
        border: 1px solid #2a2a4a;
        transition: transform 0.3s;
    }
    
    .FeatureCard:hover {
        transform: translateY(-5px);
        border-color: #4a4aff;
    }
    
    /* CTA buttons */
    .CTA-Button {
        background: linear-gradient(90deg, #4a4aff, #6a6aff);
        padding: 15px 40px;
        border-radius: 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        cursor: pointer;
    }
    
    /* Pricing cards */
    .PricingCard {
        padding: 30px;
        background: #0f0f23;
        border-radius: 15px;
        border: 2px solid #2a2a4a;
        text-align: center;
    }
    
    .PricingCard.featured {
        border-color: #4a4aff;
    }
</style>
""", unsafe_allow_html=True)


# SEO Meta Tags (rendered as HTML)
st.markdown("""
<!-- SEO Metadata -->
<meta name="description" content="AI-powered web crawling service with LangGraph SDK. Crawl websites at scale with Firecrawl, Crawl4AI. Multiple modes: single page, depth, sitemap, knowledge graph, deep crawl.">
<meta name="keywords" content="web crawler, ai crawler, firecrawl, crawl4ai, web scraping, langgraph, knowledge graph, sitemap crawler, deep crawl, seo crawler">
<meta name="author" content="Web Crawler Agent">
<meta property="og:title" content="Web Crawler Agent - AI-Powered Web Crawling">
<meta property="og:description" content="Crawl websites at scale with AI. Multiple providers, 5 crawl modes, billing included.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Web Crawler Agent">
<meta name="twitter:description" content="AI-powered web crawling with LangGraph SDK">
""", unsafe_allow_html=True)


# Hero Section
st.markdown("""
<div class="Hero">
    <h1 style="font-size: 60px; margin-bottom: 20px;">🕷️ Web Crawler Agent</h1>
    <h2 style="font-size: 28px; color: #a0a0c0; margin-bottom: 30px;">
        AI-Powered Web Crawling Service
    </h2>
    <p style="font-size: 18px; color: #808090; max-width: 600px; margin: 0 auto 40px;">
        Crawl websites at scale with multiple providers. Firecrawl, Crawl4AI, and more.
        Single page, depth, sitemap, knowledge graph, or deep crawl modes.
    </p>
    <div style="display: flex; gap: 20px; justify-content: center;">
        <a href="/chat" target="_self" style="text-decoration: none;">
            <button class="CTA-Button">🚀 Start Crawling Free</button>
        </a>
        <a href="#pricing" style="text-decoration: none;">
            <button style="padding: 15px 40px; border-radius: 30px; font-size: 18px; background: transparent; border: 2px solid #4a4aff; color: #4a4aff; cursor: pointer;">View Pricing</button>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)


# Stats
st.markdown("### ")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Crawl Providers", "3+", "Firecrawl, Crawl4AI")
with col2:
    st.metric("Crawl Modes", "5", "Single to Deep")
with col3:
    st.metric("Pages Crawled", "1M+", "This month")
with col4:
    st.metric("Uptime", "99.9%", "Guaranteed")


# Features Section
st.markdown("## ✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="FeatureCard">
        <h3>🕷️ Multiple Providers</h3>
        <p>Choose from Firecrawl, Crawl4AI, or deploy your own. Open source compatible.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="FeatureCard">
        <h3>📊 5 Crawl Modes</h3>
        <p>Single, Depth, Sitemap, Knowledge Graph, Deep Crawl. Pick what you need.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="FeatureCard">
        <h3>💳 Built-in Billing</h3>
        <p>Credits, subscriptions, usage metering. All in one dashboard.</p>
    </div>
    """, unsafe_allow_html=True)


# Use Cases
st.markdown("## 🎯 Use Cases")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### SEO & Marketing
    - Crawl competitor sites
    - Build sitemap for SEO
    - Monitor pricing & content
    - Research backlinks
    """)

with col2:
    st.markdown("""
    ### Data & Research
    - Extract knowledge graphs
    - Build training datasets
    - Monitor news & trends
    - Academic research
    """)


# Pricing Section
st.markdown("## 💰 Pricing")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="PricingCard">
        <h3>🆓 Free</h3>
        <h2>$0</h2>
        <p>100 credits/month</p>
        <p>100 pages max</p>
        <button style="margin-top: 20px; padding: 10px 30px; border-radius: 20px; background: #2a2a4a; border: none; color: white; cursor: pointer;">Get Started</button>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="PricingCard featured">
        <h3>🚀 Starter</h3>
        <h2>$29/mo</h2>
        <p>1,000 credits</p>
        <p>10,000 pages</p>
        <button style="margin-top: 20px; padding: 10px 30px; border-radius: 20px; background: #4a4aff; border: none; color: white; cursor: pointer;">Start Trial</button>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="PricingCard">
        <h3>⚡ Pro</h3>
        <h2>$99/mo</h2>
        <p>10,000 credits</p>
        <p>100,000 pages</p>
        <button style="margin-top: 20px; padding: 10px 30px; border-radius: 20px; background: #2a2a4a; border: none; color: white; cursor: pointer;">Upgrade</button>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="PricingCard">
        <h3>🏢 Enterprise</h3>
        <h2>Custom</h2>
        <p>Unlimited credits</p>
        <p>Unlimited pages</p>
        <button style="margin-top: 20px; padding: 10px 30px; border-radius: 20px; background: #2a2a4a; border: none; color: white; cursor: pointer;">Contact Us</button>
    </div>
    """, unsafe_allow_html=True)


# API Example
st.markdown("## 🔧 Developer API")

st.code("""
# Install
pip install crawler-agent

# Use
from crawler_agent import CrawlAgent

agent = CrawlAgent(provider="crawl4ai")
result = await agent.crawl(
    "https://example.com",
    mode="knowledge",
    depth=3
)

print(result)
""", language="python")


# Testimonials (placeholder)
st.markdown("## 💬 What People Say")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    > "Best web crawler I've used. The knowledge graph mode is incredible for SEO research."
    > — **Marketing Director**, TechCorp
    """)

with col2:
    st.markdown("""
    > "Finally, a crawler that just works. Fast, reliable, and the billing is simple."
    > — **Founder**, DataStartup
    """)


# CTA Section
st.markdown("""
<div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 20px; margin: 40px 0;">
    <h2>Ready to start crawling?</h2>
    <p style="color: #a0a0c0; margin: 20px 0;">Get 100 free credits when you sign up.</p>
    <button class="CTA-Button">🚀 Get Started Free</button>
</div>
""", unsafe_allow_html=True)


# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🕷️ Web Crawler Agent
    
    AI-powered web crawling service for developers and businesses.
    """)

with col2:
    st.markdown("""
    ### Links
    - [Documentation](/docs)
    - [API Reference](/api)
    - [Status Page](https://status.example.com)
    """)

with col3:
    st.markdown("""
    ### Legal
    - [Privacy Policy](/privacy)
    - [Terms of Service](/terms)
    - [Contact](/contact)
    """)

st.markdown(f"""
---
© {datetime.now().year} Web Crawler Agent. All rights reserved.
""")


if __name__ == "__main__":
    st.run()