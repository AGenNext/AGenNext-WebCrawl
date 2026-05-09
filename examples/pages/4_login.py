"""Login and Authentication Page

Simple login page for the web crawler service with billing.
"""
import streamlit as st
import hashlib
import uuid
from datetime import datetime, timedelta

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
    page_title="Login - Web Crawler",
    page_icon="🔐",
    layout="centered",
)


# Simple session state for demo (use database in production)
if "users" not in st.session_state:
    st.session_state.users = {
        "demo@user.com": {
            "password_hash": hashlib.sha256(b"demo123").hexdigest(),
            "name": "Demo User",
            "user_id": "user_demo",
            "plan": "free",
            "credits": 100,
        }
    }

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


def create_session_token() -> str:
    return str(uuid.uuid4())


# UI
st.title("🔐 Login to Crawler Service")
st.markdown("Access your web crawling dashboard")

# Show login form or dashboard based on auth state
if not st.session_state.authenticated:
    
    # Login form
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button("Login", use_container_width=True)
        with col2:
            register = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit and email and password:
            if email in st.session_state.users:
                user = st.session_state.users[email]
                if verify_password(password, user["password_hash"]):
                    st.session_state.authenticated = True
                    st.session_state.current_user = email
                    st.rerun()
                else:
                    st.error("Invalid password")
            else:
                st.error("User not found. Create an account or use demo@user.com / demo123")
        
        if register:
            st.info("Redirecting to registration...")
    
    st.divider()
    
    # Demo credentials
    st.caption("Demo: `demo@user.com` / `demo123`")
    
    # Alternative: OAuth buttons
    st.divider()
    st.markdown("**Or continue with:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("🔗 Google", use_container_width=True, disabled=True)
    with col2:
        st.button("🐙 GitHub", use_container_width=True, disabled=True)  
    with col3:
        st.button("📧 Email", use_container_width=True, disabled=True)

else:
    # Show user dashboard after login
    st.success(f"Welcome back, {st.session_state.users[st.session_state.current_user]['name']}!")
    
    user = st.session_state.users[st.session_state.current_user]
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Credits", user.get("credits", 0))
    with col2:
        st.metric("Plan", user.get("plan", "free").title())
    with col3:
        st.metric("Pages Used", 0)
    
    st.divider()
    
    # Quick actions
    st.subheader("Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Start Crawling", use_container_width=True):
            st.info("Open the crawler dashboard")
    with col2:
        if st.button("💳 Buy Credits", use_container_width=True):
            st.info("Open billing")
    
    st.divider()
    
    # Logout
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()


# Registration form (shown when clicking Create Account)
if st.session_state.get("show_register", False):
    st.divider()
    st.header("Create Account")
    
    with st.form("register_form"):
        new_name = st.text_input("Name")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        
        if st.form_submit_button("Create Account"):
            if new_email in st.session_state.users:
                st.error("Email already exists")
            elif new_password != confirm:
                st.error("Passwords don't match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                # Create user
                st.session_state.users[new_email] = {
                    "password_hash": hash_password(new_password),
                    "name": new_name,
                    "user_id": f"user_{uuid.uuid4().hex[:8]}",
                    "plan": "free",
                    "credits": 0,
                }
                st.success("Account created! Please login.")
                st.session_state.show_register = False


# Forgot password
with st.expander("Forgot Password?"):
    st.write("Reset your password")
    reset_email = st.text_input("Enter your email")
    if st.button("Send Reset Link"):
        st.info(f"Reset link sent to {reset_email} (demo only)")


# Footer
st.divider()
st.caption("Web Crawler Service v0.1.0")


if __name__ == "__main__":
    st.run()