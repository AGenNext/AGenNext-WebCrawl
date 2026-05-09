"""Account Management Page

User account settings, profile, API keys, and team management.
"""
import streamlit as st
import hashlib
import uuid
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
    page_title="Account Settings",
    page_icon="👤",
    layout="wide",
)


st.title("👤 Account Settings")
st.markdown("Manage your account, API keys, and team")


# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Profile", "🔑 API Keys", "🔔 Notifications", "👥 Team", "🗑️ Danger Zone"
])


with tab1:
    st.header("Profile Settings")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value="Demo User")
            email = st.text_input("Email", value="demo@user.com")
        
        with col2:
            company = st.text_input("Company", value="My Company")
            phone = st.text_input("Phone", placeholder="+1 (555) 123-4567")
        
        # Avatar
        st.divider()
        st.subheader("Avatar")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://api.dicebear.com/7.x/initials/svg?seed=DU", width=100)
        with col2:
            uploaded = st.file_uploader("Upload new avatar", type=["png", "jpg"])
            if uploaded:
                st.success("Avatar uploaded!")
        
        st.divider()
        st.form_submit_button("Save Changes")


# API Keys
with tab2:
    st.header("API Keys")
    st.info("Use API keys to access the crawler programmatically")
    
    # Existing keys
    st.subheader("Your API Keys")
    
    keys = [
        {
            "name": "Production",
            "key": "fc_live_xxxxxxxxxxxxx",
            "created": "2024-01-01",
            "last_used": "2024-01-15",
        },
        {
            "name": "Development", 
            "key": "fc_test_xxxxxxxxxxxxx",
            "created": "2024-01-05",
            "last_used": "Never",
        },
    ]
    
    for k in keys:
        with st.expander(f"{k['name']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.code(k["key"], language=None)
            with col2:
                if st.button("Copy", key=f"copy_{k['name']}"):
                    st.copy_to_clipboard(k["key"])
                    st.success("Copied!")
            
            st.caption(f"Created: {k['created']}")
            st.caption(f"Last used: {k['last_used']}")
            
            if st.button(f"Regenerate {k['name']}", key=f"regen_{k['name']}"):
                st.warning("Regenerate? This will invalidate the old key.")
    
    st.divider()
    
    # Create new key
    st.subheader("Create New Key")
    
    with st.form("key_form"):
        key_name = st.text_input("Key Name", placeholder="My API Key")
        key权限 = st.multiselect(
            "Permissions",
            ["crawl", "search", "billing", "admin"],
            default=["crawl"]
        )
        
        if st.form_submit_button("Create API Key"):
            st.success("API key created!")
            st.code(f"fc_live_{uuid.uuid4().hex[:24]}", language=None)
            st.warning("⚠️ Save this key - it won't be shown again!")


# Notifications
with tab3:
    st.header("Notification Settings")
    
    with st.form("notif_form"):
        st.subheader("Email Notifications")
        
        crawl_complete = st.toggle("Crawl Complete", value=True)
        credits_low = st.toggle("Low Credits Alert", value=True)
        usage_alerts = st.toggle("Usage Alerts", value=True)
        marketing = st.toggle("Marketing Emails", value=False)
        
        st.divider()
        
        st.subheader("In-App Notifications")
        
        show_crawl = st.toggle("Show Crawl Progress", value=True)
        show_errors = st.toggle("Show Errors", value=True)
        
        st.divider()
        
        st.form_submit_button("Save Preferences")
    
    st.divider()
    
    # Email preferences
    st.subheader("Email Frequency")
    
    frequency = st.radio(
        "When to send digest",
        ["Instant", "Daily", "Weekly", "Never"],
        horizontal=True
    )


# Team
with tab4:
    st.header("Team Management")
    st.info("Invite team members to collaborate")
    
    # Invite form
    st.subheader("Invite Team Member")
    
    with st.form("invite_form"):
        invite_email = st.text_input("Email Address")
        role = st.selectbox("Role", ["Member", "Admin", "Viewer"])
        
        if st.form_send_button("Send Invite"):
            st.success(f"Invite sent to {invite_email}")
    
    st.divider()
    
    # Team members
    st.subheader("Team Members")
    
    members = [
        {"name": "Demo User", "email": "demo@user.com", "role": "Admin", "status": "Active"},
        {"name": "John Doe", "email": "john@company.com", "role": "Member", "status": "Active"},
    ]
    
    for member in members:
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            st.write(f"**{member['name']}**")
            st.caption(member['email'])
        with col2:
            st.write(member['role'])
        with col3:
            st.caption(member['status'])
        with col4:
            if member["role"] != "Admin":
                if st.button("Remove", key=f"remove_{member['email']}"):
                    st.warning("Remove member?")


# Danger Zone
with tab5:
    st.header("🗑️ Danger Zone")
    st.error("These actions are irreversible!")
    
    # Delete account
    st.subheader("Delete Account")
    st.warning("Once you delete your account, there is no going back.")
    
    with st.form("delete_form"):
        confirm = st.text_input("Type 'DELETE' to confirm")
        
        if st.form_submit_button("Delete My Account"):
            if confirm == "DELETE":
                st.error("Account deleted!")
            else:
                st.error("Type 'DELETE' to confirm")
    
    st.divider()
    
    # Export data
    st.subheader("Export Data")
    st.warning("Download all your data before deleting.")
    
    if st.button("Export All Data"):
        st.info("Preparing export...")
    
    st.divider()
    
    # Cancel subscription
    st.subheader("Cancel Subscription")
    st.warning("You will lose access to premium features.")
    
    if st.button("Cancel Subscription"):
        st.warning("Are you sure?")


# Sidebar - Account info
with st.sidebar:
    st.header("Account")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://api.dicebear.com/7.x/initials/svg?seed=DU", width=50)
    with col2:
        st.write("**Demo User**")
        st.caption("Free Plan")
    
    st.divider()
    
    # Usage
    st.caption("**This Month:**")
    st.metric("Pages Used", "45 / 100")
    st.metric("Credits", "55")
    
    st.divider()
    
    # Billing link
    if st.button("💳 Manage Billing"):
        st.info("Open billing page")


if __name__ == "__main__":
    st.run()