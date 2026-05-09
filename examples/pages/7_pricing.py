"""
Pricing Page - Web Crawler Service

Shows pricing plans and credit packages.
"""
import streamlit as st
import sys
sys.path.insert(0, '/workspace/project')
from version import __version__, APP_TITLE
from components.seo_meta import add_seo_meta, get_seo_config, DEFAULT_DESCRIPTION


def main():
    # SEO
    seo = get_seo_config("Pricing")
    st.set_page_config(
        page_title=seo["page_title"],
        page_icon="💰",
        layout="wide",
    )
    add_seo_meta("Pricing", "Pricing plans for Web Crawler Service")
    
    st.title("💰 Pricing")
    st.markdown("Simple, transparent pricing for everyone")
    
    st.divider()
    
    # Plans
    st.header("📦 Plans")
    
    # CSS for cards
    st.markdown("""
    <style>
    .plan-card {
        padding: 20px;
        border-radius: 10px;
        background: #f0f2f6;
        text-align: center;
    }
    .plan-card:hover {
        background: #e8eaf0;
    }
    .popular-badge {
        background: #FF4B4B;
        color: white;
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Free
    with col1:
        st.markdown("### 🆓 Free")
        st.markdown("#### $0/month")
        st.markdown("""
        - 100 pages/month
        - Single page mode
        - Basic support
        - Community access
        """)
        st.button("Get Started", key="free_btn", use_container_width=True)
    
    # Pro - Popular
    with col2:
        st.markdown('<span class="popular-badge">MOST POPULAR</span>', unsafe_allow_html=True)
        st.markdown("### ⚡ Pro")
        st.markdown("#### $29/month")
        st.markdown("""
        - 10,000 pages/month
        - All crawl modes
        - Priority support
        - API access
        - Custom agents
        """)
        st.button("Upgrade to Pro", key="pro_btn", type="primary", use_container_width=True)
    
    # Enterprise
    with col3:
        st.markdown("### 🏢 Enterprise")
        st.markdown("#### Custom")
        st.markdown("""
        - Unlimited pages
        - Dedicated instance
        - 24/7 support
        - SLA guarantee
        - Custom integrations
        """)
        st.button("Contact Sales", key="ent_btn", use_container_width=True)
    
    st.divider()
    
    # Credits
    st.header("🎫 Credit Packages")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### Starter")
        st.markdown("#### $10")
        st.caption("= 1,000 credits (~1,000 pages)")
        st.progress(100, text="💎")
        st.button("Buy Starter Pack", key="buy1", use_container_width=True)
    
    with c2:
        st.markdown("### Standard")
        st.markdown("#### $50")
        st.caption("= 6,000 credits (~6,000 pages)")
        st.progress(100, text="💎")
        st.markdown("🔥 **Save 20%**")
        st.button("Buy Standard Pack", key="buy2", use_container_width=True)
    
    with c3:
        st.markdown("### Premium")
        st.markdown("#### $100")
        st.caption("= 15,000 credits (~15,000 pages)")
        st.progress(100, text="💎")
        st.markdown("🔥 **Save 50%**")
        st.button("Buy Premium Pack", key="buy3", use_container_width=True)
    
    st.divider()
    
    # Comparison
    st.header("📊 Feature Comparison")
    
    st.table({
        "Feature": ["Crawl Modes", "Pages/Month", "API Access", "Priority Support", "Custom Agents"],
        "Free": ["Single", "100", "❌", "❌", "❌"],
        "Pro": ["All", "10,000", "✅", "✅", "✅"],
        "Enterprise": ["All", "∞", "✅", "✅", "✅"],
    })
    
    st.divider()
    
    # FAQ
    st.header("❓ FAQ")
    
    with st.expander("How do credits work?"):
        st.markdown("""
        **Each page crawl costs 1 credit.** Deep crawl mode uses more 
        credits based on number of pages crawled. Unused credits roll 
        over to the next billing month.
        """)
    
    with st.expander("Can I change plans anytime?"):
        st.markdown("""
        Yes! You can upgrade or downgrade your plan at any time. 
        Upgrades take effect immediately, downgrades apply at the 
        next billing cycle.
        """)
    
    with st.expander("Do you offer refunds?"):
        st.markdown("""
        We offer a **30-day money-back guarantee** for all paid plans. 
        Contact support for refund requests.
        """)
    
    with st.expander("What payment methods?"):
        st.markdown("""
        We accept **Visa, MasterCard, Amex, PayPal**, and **wire transfers** 
        for enterprise plans.
        """)
    
    with st.expander("Is there a trial?"):
        st.markdown("""
        Yes! The **Free plan** lets you test the service with no 
        commitment. No credit card required.
        """)


if __name__ == "__main__":
    main()