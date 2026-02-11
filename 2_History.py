import streamlit as st
import pandas as pd
from utils.auth import require_auth, get_current_user

require_auth()

st.set_page_config(page_title="History", page_icon="🕘", layout="wide")

# Styling
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.history-card {
    background:#0f1729;
    border:1px solid #1f2937;
    border-radius:10px;
    padding:16px;
    margin:10px 0;
}
.status-success {color:#10b981;}
.status-error {color:#ef4444;}
</style>
""", unsafe_allow_html=True)

user = get_current_user()

# Header
col1, col2 = st.columns([8, 2])
with col1:
    st.title("🕘 Optimization History")
    st.caption("View and manage your past code optimizations")
with col2:
    st.write(f"👤 **{user['username']}**")

st.markdown("---")

# Get history from session state
history = st.session_state.get("history", [])

if history:
    # Filters
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    with col_filter1:
        filter_mode = st.selectbox(
            "Filter by Mode:",
            ["All", "HYBRID", "RULES_ONLY"]
        )
    with col_filter2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Date (Newest)", "Date (Oldest)", "Speedup (Highest)"]
        )
    with col_filter3:
        search = st.text_input("🔍 Search by Job ID:", placeholder="CF-20250204-...")
    
    # Convert to DataFrame
    df = pd.DataFrame(history)
    
    # Apply filters
    if filter_mode != "All":
        df = df[df["Mode"] == filter_mode]
    
    if search:
        df = df[df["Job ID"].str.contains(search, case=False, na=False)]
    
    # Apply sorting
    if "Date" in df.columns:
        if sort_by == "Date (Newest)":
            df = df.sort_values("Date", ascending=False)
        elif sort_by == "Date (Oldest)":
            df = df.sort_values("Date", ascending=True)
        elif sort_by == "Speedup (Highest)" and "Speedup" in df.columns:
            # Extract numeric speedup value
            df["speedup_num"] = df["Speedup"].str.replace("x", "").str.replace("N/A", "0").astype(float)
            df = df.sort_values("speedup_num", ascending=False)
            df = df.drop("speedup_num", axis=1)
    
    # Display results
    st.markdown(f"### 📊 Showing {len(df)} results")
    
    if len(df) > 0:
        # Display as styled table
        st.dataframe(
            df,
            use_container_width=True,
            height=400,
            column_config={
                "Job ID": st.column_config.TextColumn("Job ID", width="medium"),
                "Date": st.column_config.TextColumn("Date", width="medium"),
                "Mode": st.column_config.TextColumn("Mode", width="small"),
                "Speedup": st.column_config.TextColumn("Speedup", width="small"),
                "Status": st.column_config.TextColumn("Status", width="small"),
            }
        )
        
        # Export functionality
        st.markdown("---")
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Export to CSV",
            csv,
            "codeforge_history.csv",
            "text/csv",
            use_container_width=False
        )
        
        # Clear history button (admin only)
        if user.get("role") == "admin":
            if st.button("🗑 Clear All History", type="secondary"):
                if st.warning("Are you sure? This cannot be undone."):
                    st.session_state.history = []
                    st.rerun()
    else:
        st.info("No results match your filters.")
    
    # Statistics
    st.markdown("---")
    st.markdown("### 📈 Statistics")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        total_opts = len(history)
        st.metric("Total Optimizations", total_opts)
    
    with stat_col2:
        hybrid_count = sum(1 for h in history if h.get("Mode") == "HYBRID")
        st.metric("AI-Powered", hybrid_count)
    
    with stat_col3:
        rules_count = sum(1 for h in history if h.get("Mode") == "RULES_ONLY")
        st.metric("Rules-Only", rules_count)
    
    with stat_col4:
        success_rate = sum(1 for h in history if "Success" in h.get("Status", "")) / len(history) * 100
        st.metric("Success Rate", f"{success_rate:.1f}%")

else:
    st.info("📭 No optimization history yet.")
    st.markdown("""
    Your optimization history will appear here once you start optimizing code.
    
    **Get started:**
    1. Go to the [Dashboard](1_Dashboard)
    2. Paste your Python code
    3. Click "Optimize Code"
    """)

st.markdown("---")
st.caption("© 2025 CodeForge | History is stored locally in your session")
