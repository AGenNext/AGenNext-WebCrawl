"""Billing Dashboard Page

This is a Next.js page for the billing dashboard.
It provides a web interface for managing subscriptions, credits, and usage.
"""
import streamlit as st
import asyncio
from datetime import datetime

st.set_page_config(
    page_title="$f",
    page_icon="🕷️",
    layout="wide",
)

# SEO
st.markdown("""<head>
    <meta name="description" content="AGenNext - AI-powered web crawling service">
    <meta name="keywords" content="web crawler, web scraping, AI scraping">
</head>""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Crawler Billing Dashboard",
    page_icon="💳",
    layout="wide",
)

st.title("💳 Billing Dashboard")
st.markdown("Manage your subscriptions, credits, and usage")


# Sidebar - User Info
st.sidebar.header("User Settings")

user_id = st.sidebar.text_input("User ID", value="user123")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💎 Credits", "📦 Plans", "📈 Usage"])


with tab1:
    st.header("Account Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Credits", 150)
    
    with col2:
        st.metric("Pages Used", 45)
    
    with col3:
        st.metric("Subscription", "Free")
    
    st.divider()
    
    # Quick actions
    st.subheader("Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Add 100 Credits ($5)", use_container_width=True):
            st.success("Added 100 credits!")
    
    with col2:
        if st.button("Upgrade Plan", use_container_width=True):
            st.info("Redirecting to plans...")


with tab2:
    st.header("Credit Management")
    
    # Buy credits
    st.subheader("Buy Credits")
    
    col1, col2, col3 = st.columns(3)
    
    packages = [
        {"name": "Starter", "credits": 100, "price": 5, "bonus": 5},
        {"name": "Basic", "credits": 500, "price": 20, "bonus": 50},
        {"name": "Pro", "credits": 1000, "price": 35, "bonus": 150},
    ]
    
    for i, pkg in enumerate(packages):
        with [col1, col2, col3][i]:
            st.metric(
                pkg["name"],
                f"{pkg['credits'] + pkg['bonus']} credits",
                f"${pkg['price']}",
            )
            if st.button(f"Buy {pkg['name']}", key=f"buy_{i}"):
                st.success(f"Purchased {pkg['name']}!")
    
    st.divider()
    
    # Credit history
    st.subheader("Transaction History")
    
    transactions = [
        {"date": "2024-01-15", "type": "Purchase", "credits": 100, "amount": 5},
        {"date": "2024-01-10", "type": "Usage", "credits": -10, "amount": 0},
        {"date": "2024-01-05", "type": "Bonus", "credits": 50, "amount": 0},
    ]
    
    for tx in transactions:
        st.write(f"{tx['date']} - {tx['type']}: {tx['credits']:+d} credits")


with tab3:
    st.header("Subscription Plans")
    
    st.info("💡 Subscription gives you monthly page limits instead of prepaying")
    
    plans = [
        {
            "name": "Free",
            "price": "$0/mo",
            "pages": 100,
            "depth": 1,
            "modes": ["single"],
        },
        {
            "name": "Starter",
            "price": "$19/mo",
            "pages": 1000,
            "depth": 2,
            "modes": ["single", "depth"],
        },
        {
            "name": "Pro",
            "price": "$49/mo",
            "pages": 10000,
            "depth": 5,
            "modes": ["single", "depth", "sitemap", "knowledge"],
        },
        {
            "name": "Enterprise",
            "price": "$199/mo",
            "pages": "Unlimited",
            "depth": "Unlimited",
            "modes": ["all"],
        },
    ]
    
    for plan in plans:
        with st.expander(f"{plan['name']} - {plan['price']}"):
            st.write(f"**Pages:** {plan['pages']}")
            st.write(f"**Max Depth:** {plan['depth']}")
            st.write(f"**Modes:** {', '.join(plan['modes'])}")
            
            if plan["name"] != "Free":
                if st.button(f"Upgrade to {plan['name']}", key=f"upgrade_{plan['name']}"):
                    st.success(f"Upgraded to {plan['name']}!")
    


with tab4:
    st.header("Usage Statistics")
    
    # Usage chart (placeholder)
    st.subheader("Pages This Month")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Pages", 45)
    
    with col2:
        st.metric("Total Calls", 12)
    
    with col3:
        st.metric("Data Transferred", "1.2 MB")
    
    st.divider()
    
    # Recent crawls
    st.subheader("Recent Crawls")
    
    crawls = [
        {"date": "2024-01-15", "url": "example.com", "mode": "depth", "pages": 3},
        {"date": "2024-01-14", "url": "httpbin.org", "mode": "single", "pages": 1},
        {"date": "2024-01-13", "url": "example.org", "mode": "knowledge", "pages": 2},
    ]
    
    for crawl in crawls:
        st.write(f"{crawl['date']} - {crawl['url']} ({crawl['mode']}, {crawl['pages']} pages)")


# API Reference
st.divider()
st.header("API Reference")

with st.expander("View API Documentation"):
    st.code("""
# Add Credits
POST /api/billing/credits
{"user_id": "user123", "credits": 100}

# Check Balance  
GET /api/billing/credits/user123

# Get Usage
GET /api/billing/usage/user123?month=1&year=2024

# Upgrade Plan
POST /api/billing/upgrade
{"user_id": "user123", "plan": "pro"}
    """, language="python")


if __name__ == "__main__":
    st.run()