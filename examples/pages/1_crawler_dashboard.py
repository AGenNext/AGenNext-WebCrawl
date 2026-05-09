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
    st.session_state.user = None


# ============== LOGIN CHECK ==============
def check_auth():
    """Require authentication"""
    if not st.session_state.authenticated:
        st.markdown("""
        <div style='text-align:center; padding:3rem'>
            <h1>🔐 Login Required</h1>
            <p>Please login to access the crawler</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("📧 Email")
            with col2:
                password = st.text_input("🔑 Password", type="password")
            
            if st.form_submit_button("Login", type="primary"):
                # Demo creds
                if email == "demo@agennext.com" and password == "demo123":
                    st.session_state.authenticated = True
                    st.session_state.user = {"email": email, "plan": "free", "credits": 100}
                    st.rerun()
                else:
                    st.error("Invalid credentials (demo@agennext.com / demo123)")
        st.stop()


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
    "openai": {"name": "🤖 OpenAI", "models": ["gpt-4o", "o1-preview"]},
    "anthropic": {"name": "🧠 Claude", "models": ["sonnet-4", "opus-4"]},
    "ollama": {"name": "🦙 Ollama", "models": ["llama3", "mistral"]},
    "gemini": {"name": "✨ Gemini", "models": ["gemini-2.0", "gemini-pro"]},
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
    
    # Quick config
    st.subheader("⚙️ Configuration")
    provider = st.selectbox("Crawler", list(CRAWL_PROVIDERS.keys()), format_func=lambda x: CRAWL_PROVIDERS[x]["name"])
    llm = st.selectbox("LLM", list(LLM_PROVIDERS.keys()), format_func=lambda x: LLM_PROVIDERS[x]["name"])
    
    st.divider()
    
    # Account from session
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
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url = st.text_input("🌐 Website URL", placeholder="https://example.com")
    
    with col2:
        mode = st.selectbox("📊 Mode", list(CRAWL_MODES.keys()), format_func=lambda x: CRAWL_MODES[x])
    
    # Options
    col3, col4, col5 = st.columns(3)
    
    with col3:
        max_pages = st.slider("📄 Max Pages", 1, 100, 10)
    
    with col4:
        max_depth = st.number_input("📏 Depth", 1, 10, 2)
    
    with col5:
        timeout = st.number_input("⏱️ Timeout (s)", 10, 300, 60)
    
    # Submit
    col_submit, _ = st.columns([1, 3])
    with col_submit:
        submitted = st.form_submit_button("🚀 Start Crawl", use_container_width=True, type="primary")


# Process
if submitted and url:
    st.success(f"✅ Crawl started: {url}")
    st.info(f"Mode: {CRAWL_MODES[mode]} | Pages: {max_pages} | Depth: {max_depth}")


# Results preview
if "url" in locals() and submitted:
    with st.expander("📊 Results", expanded=True):
        col_r1, col_r2, col_r3 = st.columns(3)
        
        with col_r1:
            st.metric("Pages", 0)
        
        with col_r2:
            st.metric("Links", 0)
        
        with col_r3:
            st.metric("Status", "Ready")


# Footer
st.divider()
st.caption("🔵 Powered by LangGraph SDK • Crawl4AI • Firecrawl")