"""Enterprise Crawler Dashboard - Professional Web UI"""
import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Web Crawler | AGenNext",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session init
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    # Auto-login as demo on first load
    st.session_state.user = {"email": "demo@agennext.com", "plan": "free", "credits": 100}


# ============== LOGIN CHECK ==============
def check_auth():
    """Optional login - demo mode available"""
    if not st.session_state.get("user"):
        st.session_state.user = {"email": "demo@agennext.com", "plan": "free", "credits": 100}


# Check auth
check_auth()


# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    :root {
        --primary: #3b82f6;
        --primary-hover: #2563eb;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --border: #334155;
    }
    
    .stApp { font-family: 'Inter', sans-serif; }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    div[data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 8px !important;
    }
    
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ============== CONFIG ==============
CRAWL_PROVIDERS = {
    "crawl4ai": {"name": "🟡 Crawl4AI", "desc": "Open source"},
    "firecrawl": {"name": "🔥 Firecrawl", "desc": "Cloud API"},
}

LLM_PROVIDERS = {
    "ollama": {"name": "🦙 Ollama", "models": ["llama3", "mistral"]},  # FREE - default
    "openai": {"name": "🤖 OpenAI", "models": ["gpt-4o"]},
    "anthropic": {"name": "🧠 Claude", "models": ["sonnet"]},
}

CRAWL_MODES = {
    "single": "📄 Single Page",
    "depth": "📊 Depth Crawl",
    "sitemap": "🗺️ Sitemap",
    "knowledge": "🔗 Knowledge Graph",
    "deep": "🕸️ Deep Crawl",
}


# ============== SIDEBAR ==============
with st.sidebar:
    st.markdown("<h2 style='color:#3b82f6'>🕷️ AGenNext</h2>", unsafe_allow_html=True)
    st.caption("**Enterprise Web Crawler**")
    st.divider()
    
    # Page nav
    st.subheader("📑 Pages")
    st.page_link("examples/app.py", label="🏠 Dashboard", icon="🏠")
    st.page_link("examples/pages/2_crawl_history.py", label="📜 History", icon="📜")
    st.page_link("examples/pages/3_settings.py", label="⚙️ Settings", icon="⚙️")
    
    st.divider()
    
    # Quick config
    st.subheader("⚙️ Configuration")
    provider = st.selectbox("Crawler", list(CRAWL_PROVIDERS.keys()), format_func=lambda x: CRAWL_PROVIDERS[x]["name"])
    llm = st.selectbox("LLM", list(LLM_PROVIDERS.keys()), format_func=lambda x: LLM_PROVIDERS[x]["name"])
    mode = st.selectbox("Mode", list(CRAWL_MODES.keys()), format_func=lambda x: CRAWL_MODES[x])
    
    st.divider()
    
    # Options
    st.subheader("🔧 Options")
    max_pages = st.slider("Max Pages", 1, 100, 10)
    max_depth = st.number_input("Depth", 1, 10, 2)
    timeout = st.number_input("Timeout (s)", 10, 300, 60)
    
    st.divider()
    
    # Account
    user = st.session_state.user or {"plan": "free", "credits": 100}
    st.subheader("👤 Account")
    st.metric("Plan", user.get("plan", "Free").title())
    st.metric("Credits", user.get("credits", 100))
    
    # Logout
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()


# ============== MAIN ==============
st.title("🌐 New Web Crawl")
st.markdown("Enterprise-grade web scraping with LangGraph SDK")

# Main form
with st.form("crawl_form"):
    url = st.text_input("🌐 Website URL", placeholder="https://example.com")
    
    # Submit
    col_submit, col_cost = st.columns([1, 2])
    
    with col_submit:
        submitted = st.form_submit_button("🚀 Start Crawl", use_container_width=True, type="primary")
    
    # Cost estimate
    with col_cost:
        cost = max(1, max_pages) * {"single": 1, "depth": 2, "sitemap": 2, "knowledge": 3, "deep": 5}.get(mode, 1)
        st.caption(f"💰 Est. Cost: {cost} credits")


# Success
if submitted and url:
    st.success(f"✅ Crawl started: {url}")
    
    # Stream output
    st.subheader("📡 Live Output")
    output_area = st.empty()
    output_area.info(f"🔄 Crawling: {url}")
    
    # Simulated crawl progress (replace with actual crawl)
    import time
    for i in range(1, min(max_pages, 5) + 1):
        output_area.code(f"📄 Page {i}: {url}\n🔗 Found 3 links\n✅ Success")
        time.sleep(0.5)
    
    output_area.code(f"✅ Crawl complete!\n📄 Pages: {i}\n🔗 Links: {i * 3}")
    
    # Live metrics
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    
    with col_r1:
        st.metric("📄 Pages", i)
    
    with col_r2:
        st.metric("🔗 Links", i * 3)
    
    with col_r3:
        st.metric("💰 Cost", i)
    
    with col_r4:
        st.metric("⏱️ Status", "Done")


# Footer
st.divider()
st.caption("🔵 Powered by LangGraph SDK • Crawl4AI • Firecrawl")