import streamlit as st
import os
import json

# Page config
st.set_page_config(
    page_title="CodeForge - Login",
    page_icon="🔐",
    layout="centered"
)

# Check if already logged in
if st.session_state.get("auth", {}).get("is_auth"):
    st.switch_page("pages/1_Dashboard.py")

# Helper functions
def get_users():
    """Load users from environment or use defaults"""
    raw = os.getenv("APP_USERS_JSON", "").strip()
    if not raw:
        return [
            {"u": "admin", "p": "admin123", "role": "admin"},
            {"u": "user", "p": "user123", "role": "user"}
        ]
    try:
        return json.loads(raw)
    except Exception:
        return []

def authenticate(username, password):
    """Authenticate user credentials"""
    users = get_users()
    for rec in users:
        if rec["u"] == username and rec["p"] == password:
            return {"username": username, "role": rec.get("role", "user")}
    return None

# Styling
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.logo-section {
    text-align: center;
    margin-bottom: 40px;
}
</style>
""", unsafe_allow_html=True)

# Logo and Title
st.markdown("""
<div class='logo-section'>
    <div style='font-size: 64px; margin-bottom: 10px;'>⚙️</div>
    <h1 style='font-size: 32px; font-weight: 700; color: #3b82f6;'>CodeForge</h1>
    <p style='color: #9ca3af;'>AI-Powered Code Optimization Platform</p>
</div>
""", unsafe_allow_html=True)

# Login Form
st.markdown("### 🔐 Sign In")
st.caption("Enter your credentials to continue")

username = st.text_input("Username", placeholder="e.g., admin")
password = st.text_input("Password", type="password", placeholder="••••••••")

col1, col2 = st.columns([1, 1])
with col1:
    remember_me = st.checkbox("Remember me", value=True)

login_button = st.button("Sign In →", type="primary", use_container_width=True)

if login_button:
    if not username or not password:
        st.error("❌ Please enter both username and password")
    else:
        user = authenticate(username.strip(), password)
        if user:
            st.session_state["auth"] = {
                "is_auth": True,
                "user": user,
                "remember": remember_me
            }
            st.success("✅ Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")

# Demo credentials
st.info("""
**📝 Demo Credentials:**  
Admin: `admin` / `admin123`  
User: `user` / `user123`
""")

# Features
st.markdown("---")
st.markdown("### ✨ Features")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🤖 AI-Powered**  \nSmart optimizations using Gemini AI")
with col2:
    st.markdown("**⚡ Fast**  \nRule-based optimizations in milliseconds")
with col3:
    st.markdown("**🛡️ Safe**  \nValidation and safety checks")

st.markdown("---")
st.caption("© 2025 CodeForge | Built with ❤️ by AI & Data Science Students")