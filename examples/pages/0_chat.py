"""Chat Interface for Crawler Service

Chat with the web crawler using natural language.
"""
import streamlit as st
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
    page_title="Chat - Web Crawler",
    page_icon="💬",
    layout="wide",
)


st.title("💬 Chat Crawler")
st.markdown("Ask questions about websites in natural language")


# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hi! I'm your web crawler assistant. Ask me to crawl a website or ask questions about it.\n\n**Examples:**\n- Crawl example.com\n- What pages are on example.com?\n- Extract all links from https://example.com\n- Give me a summary of this website"}
    ]


# Display chat messages
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
if prompt := st.chat_input("Ask me to crawl a website..."):
    # Add user message
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process command
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = process_prompt(prompt)
            st.markdown(response)
    
    # Add assistant response
    st.session_state.chat_messages.append({"role": "assistant", "content": response})


def process_prompt(prompt: str) -> str:
    """Process natural language prompts"""
    prompt_lower = prompt.lower()
    
    # Check for crawl commands
    if any(word in prompt_lower for word in ["crawl", "extract", "scrape", "get", "fetch"]):
        # Try to extract URL
        import re
        url_match = re.search(r'https?://[^\s]+', prompt)
        
        if url_match:
            url = url_match.group()
            return f"I'll crawl {url} for you. Let me run that..."
        else:
            # Try common domains
            return "Could you provide the URL to crawl? Example: crawl https://example.com"
    
    # Check for questions about pages
    if any(word in prompt_lower for word in ["pages", "links", "structure"]):
        return "I'll analyze the website structure for you. Please provide a URL."
    
    # Check for summary request
    if "summary" in prompt_lower or "about" in prompt_lower:
        return "I can summarize any website. Just provide the URL!"
    
    # Default response
    return """I can help you:
- **Crawl a website:** "Crawl https://example.com"
- **Extract links:** "Get all links from [URL]"
- **Summarize:** "Summarize [URL]"
- **Analyze structure:** "What pages are on [URL]"

Just provide a URL and what you'd like to do!"""


# Sidebar - Quick Actions
with st.sidebar:
    st.header("⚡ Quick Actions")
    
    st.markdown("**Preset Commands:**")
    
    if st.button("🔍 Crawl Example.com"):
        # Add to chat
        prompt = "Crawl https://example.com"
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Process
        response = "I'll crawl example.com now..."
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    if st.button("🔗 Extract All Links"):
        prompt = "Extract all links from https://example.com"
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        response = "Extracting links from example.com..."
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    if st.button("📝 Summarize Website"):
        prompt = "Summarize https://example.com"
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        response = "Summarizing example.com..."
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    st.divider()
    
    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Chat cleared! How can I help you?"}
        ]
        st.rerun()


# API example
with st.expander("API Example"):
    st.code("""
# Chat via API
import requests

response = requests.post(
    "https://api.example.com/chat",
    json={
        "message": "Crawl https://example.com",
        "user_id": "user123"
    }
)
print(response.json())
    """, language="python")


if __name__ == "__main__":
    st.run()