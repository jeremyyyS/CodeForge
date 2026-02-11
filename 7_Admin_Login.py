import streamlit as st
from utils.auth import require_auth, get_current_user
import json

require_auth()

st.set_page_config(page_title="Admin Tools", page_icon="🔑", layout="wide")

# Styling
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.admin-banner {
    background:#7c2d12;
    border:1px solid #991b1b;
    border-radius:8px;
    padding:12px;
    margin:12px 0;
    text-align:center;
    font-weight:600;
}
.admin-card {
    background:#0f1729;
    border:1px solid #1f2937;
    border-radius:10px;
    padding:20px;
    margin:12px 0;
}
.danger-zone {
    background:#450a0a;
    border:2px solid #7f1d1d;
    border-radius:10px;
    padding:20px;
    margin:20px 0;
}
</style>
""", unsafe_allow_html=True)

user = get_current_user()

# Admin check
if user.get("role") != "admin":
    st.error("🚫 Access Denied")
    st.warning("This page is only accessible to administrators.")
    st.info("If you need admin access, please contact your system administrator.")
    st.stop()

# Header
st.markdown("<div class='admin-banner'>🔑 ADMINISTRATOR CONTROL PANEL</div>", unsafe_allow_html=True)

col1, col2 = st.columns([8, 2])
with col1:
    st.title("🔑 Admin Tools")
    st.caption("System configuration and user management")
with col2:
    st.write(f"👤 **{user['username']}**")
    st.caption(f"Role: `ADMIN`")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "👥 User Management",
    "⚙️ System Settings",
    "📊 Analytics",
    "🚨 Danger Zone"
])

# TAB 1: User Management
with tab1:
    st.markdown("### 👥 User Management")
    
    # Current users
    st.markdown("#### Active Users")
    
    # Mock user data - replace with actual database in production
    users_data = [
        {"Username": "admin", "Role": "admin", "Status": "✅ Active", "Last Login": "2025-02-04 10:30"},
        {"Username": "user", "Role": "user", "Status": "✅ Active", "Last Login": "2025-02-04 09:15"},
        {"Username": "developer", "Role": "user", "Status": "🔄 Pending", "Last Login": "Never"},
    ]
    
    import pandas as pd
    df_users = pd.DataFrame(users_data)
    st.dataframe(df_users, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Add new user
    st.markdown("#### ➕ Add New User")
    
    col_add1, col_add2, col_add3 = st.columns(3)
    
    with col_add1:
        new_username = st.text_input("Username", placeholder="johndoe")
    
    with col_add2:
        new_password = st.text_input("Password", type="password", placeholder="••••••••")
    
    with col_add3:
        new_role = st.selectbox("Role", ["user", "admin"])
    
    if st.button("➕ Create User", type="primary"):
        if new_username and new_password:
            st.success(f"✅ User '{new_username}' created successfully!")
            st.info("In production, this would save to the database.")
        else:
            st.error("Please fill in all fields")
    
    st.markdown("---")
    
    # Modify user
    st.markdown("#### ✏️ Modify User")
    
    modify_col1, modify_col2, modify_col3 = st.columns(3)
    
    with modify_col1:
        user_to_modify = st.selectbox("Select User", [u["Username"] for u in users_data])
    
    with modify_col2:
        new_role_modify = st.selectbox("New Role", ["user", "admin"], key="modify_role")
    
    with modify_col3:
        new_status = st.selectbox("Status", ["Active", "Suspended", "Pending"])
    
    if st.button("💾 Save Changes"):
        st.success(f"✅ User '{user_to_modify}' updated successfully!")

# TAB 2: System Settings
with tab2:
    st.markdown("### ⚙️ System Configuration")
    
    st.markdown("#### 🔌 Backend Configuration")
    
    setting_col1, setting_col2 = st.columns(2)
    
    with setting_col1:
        backend_url = st.text_input(
            "Backend URL",
            value="http://localhost:8000",
            help="FastAPI backend server URL"
        )
        
        api_timeout = st.number_input(
            "API Timeout (seconds)",
            min_value=10,
            max_value=300,
            value=90,
            help="Maximum time to wait for API responses"
        )
        
        max_code_length = st.number_input(
            "Max Code Length",
            min_value=1000,
            max_value=50000,
            value=10000,
            help="Maximum characters allowed in code input"
        )
    
    with setting_col2:
        enable_ai = st.checkbox("Enable AI Optimization", value=True)
        enable_benchmarking = st.checkbox("Enable Benchmarking", value=True)
        enable_safety_checks = st.checkbox("Enable Safety Validation", value=True)
        
        st.markdown("---")
        
        debug_mode = st.checkbox("Debug Mode", value=False, help="Show detailed error messages")
    
    if st.button("💾 Save Configuration", type="primary"):
        config = {
            "backend_url": backend_url,
            "api_timeout": api_timeout,
            "max_code_length": max_code_length,
            "enable_ai": enable_ai,
            "enable_benchmarking": enable_benchmarking,
            "enable_safety_checks": enable_safety_checks,
            "debug_mode": debug_mode
        }
        st.success("✅ Configuration saved successfully!")
        st.json(config)
    
    st.markdown("---")
    
    # API Keys
    st.markdown("#### 🔑 API Keys")
    st.warning("⚠️ Sensitive information - Handle with care")
    
    gemini_api_key = st.text_input(
        "Gemini API Key",
        value="AIzaSy*********************",
        type="password",
        help="Google Gemini API key for AI optimization"
    )
    
    if st.button("🔄 Update API Key"):
        st.success("✅ API key updated successfully!")

# TAB 3: Analytics
with tab3:
    st.markdown("### 📊 System Analytics")
    
    # System stats
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Total Users", "3", "+1")
    
    with stat_col2:
        st.metric("Optimizations Today", "47", "+12")
    
    with stat_col3:
        st.metric("Avg Speedup", "2.3x", "+0.2x")
    
    with stat_col4:
        st.metric("Success Rate", "96%", "+2%")
    
    st.markdown("---")
    
    # Usage over time
    st.markdown("#### 📈 Usage Trends")
    
    import plotly.express as px
    
    # Mock data
    df_usage = pd.DataFrame({
        "Date": pd.date_range("2025-01-01", periods=30, freq="D"),
        "Optimizations": [15, 20, 18, 25, 30, 28, 35, 40, 38, 45, 42, 50, 48, 55, 52, 
                         60, 58, 65, 62, 70, 68, 75, 72, 80, 78, 85, 82, 90, 88, 95]
    })
    
    fig = px.line(df_usage, x="Date", y="Optimizations", title="Daily Optimizations")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Top users
    st.markdown("#### 🏆 Top Users")
    
    top_users = pd.DataFrame({
        "User": ["admin", "developer", "user"],
        "Optimizations": [150, 95, 80],
        "Avg Speedup": ["2.5x", "2.1x", "1.9x"]
    })
    
    st.dataframe(top_users, use_container_width=True, hide_index=True)

# TAB 4: Danger Zone
with tab4:
    st.markdown("<div class='danger-zone'>", unsafe_allow_html=True)
    st.markdown("### 🚨 Danger Zone")
    st.warning("⚠️ Actions in this section are irreversible!")
    
    st.markdown("---")
    
    # Clear history
    st.markdown("#### 🗑 Clear Optimization History")
    st.info("This will permanently delete all optimization history for all users.")
    
    if st.button("🗑 Clear All History", type="secondary"):
        confirm = st.checkbox("I understand this action cannot be undone")
        if confirm:
            if st.button("⚠️ CONFIRM DELETION", type="secondary"):
                st.session_state.history = []
                st.success("✅ All history cleared")
    
    st.markdown("---")
    
    # Reset system
    st.markdown("#### 🔄 Reset System")
    st.error("This will reset all system settings to defaults.")
    
    if st.button("🔄 Reset to Defaults", type="secondary"):
        st.warning("System reset functionality - use with extreme caution")
    
    st.markdown("---")
    
    # Database operations
    st.markdown("#### 💾 Database Operations")
    
    db_col1, db_col2 = st.columns(2)
    
    with db_col1:
        if st.button("📥 Export Database"):
            st.info("Database export functionality")
    
    with db_col2:
        if st.button("🔧 Maintenance Mode"):
            st.warning("This will put the system in maintenance mode")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2025 CodeForge | Administrator Control Panel")
