import streamlit as st
from utils.auth import require_auth, get_current_user
from utils import api
import hashlib
from datetime import datetime

require_auth()

st.set_page_config(page_title="Upload Code", page_icon="📂", layout="wide")

# Styling
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.upload-area {
    border:2px dashed #3b82f6;
    border-radius:10px;
    padding:40px;
    text-align:center;
    background:#0f1729;
    margin:20px 0;
}
.file-info {
    background:#1e293b;
    padding:12px;
    border-radius:8px;
    margin:8px 0;
}
</style>
""", unsafe_allow_html=True)

user = get_current_user()

# Header
col1, col2 = st.columns([8, 2])
with col1:
    st.title("📂 Upload Code File")
    st.caption("Upload a Python file for optimization")
with col2:
    st.write(f"👤 **{user['username']}**")

st.markdown("---")

# File uploader
st.markdown("### 📤 Upload Python File")

uploaded_file = st.file_uploader(
    "Choose a .py file",
    type=["py"],
    help="Upload a Python file (max 10,000 characters)"
)

if uploaded_file:
    # Read file content
    try:
        file_content = uploaded_file.read().decode("utf-8")
        file_size = len(file_content)
        file_lines = len(file_content.splitlines())
        
        # Display file info
        st.success(f"✅ File uploaded: **{uploaded_file.name}**")
        
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("File Size", f"{file_size} bytes")
        with col_info2:
            st.metric("Lines of Code", file_lines)
        with col_info3:
            file_hash = hashlib.md5(file_content.encode()).hexdigest()[:8]
            st.metric("File Hash", file_hash)
        
        # Show file preview
        st.markdown("### 👀 File Preview")
        with st.expander("Click to view code", expanded=True):
            st.code(file_content, language="python", line_numbers=True)
        
        # Validation
        if file_size > 10000:
            st.error("❌ File too large! Maximum size is 10,000 characters.")
            st.stop()
        
        # Optimization options
        st.markdown("---")
        st.markdown("### ⚙️ Optimization Options")
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            opt_mode = st.radio(
                "Optimization Mode:",
                ["🤖 AI-Powered (Recommended)", "⚡ Rules-Only (Fast)"],
                help="AI-Powered uses Gemini for best results. Rules-Only is faster but less comprehensive."
            )
        
        with col_opt2:
            auto_download = st.checkbox(
                "Auto-download optimized code",
                value=True,
                help="Automatically download the optimized file after processing"
            )
        
        # Optimize button
        st.markdown("---")
        col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 6])
        
        with col_btn1:
            optimize_btn = st.button(
                "🚀 Optimize File",
                type="primary",
                use_container_width=True
            )
        
        with col_btn2:
            cancel_btn = st.button(
                "❌ Cancel",
                use_container_width=True
            )
        
        if cancel_btn:
            st.rerun()
        
        # Process optimization
        if optimize_btn:
            with st.spinner("🔄 Optimizing your code..."):
                if opt_mode == "🤖 AI-Powered (Recommended)":
                    result = api.api_client.upload_file(file_content, uploaded_file.name)
                else:
                    result = api.api_client.optimize_rules_only(file_content, simple=False)
            
            if result.get("status") == "SUCCESS":
                st.markdown("---")
                st.success("✅ Optimization Complete!")
                
                # Display results in tabs
                tab1, tab2, tab3 = st.tabs(["📊 Results", "📄 Code Comparison", "💾 Download"])
                
                with tab1:
                    # Performance metrics
                    benchmarks = result.get("benchmarks", {})
                    if benchmarks:
                        st.markdown("### 📈 Performance Improvements")
                        
                        speedup = benchmarks.get("speedup_factor", 1.0)
                        orig_bench = benchmarks.get("original", {})
                        opt_bench = benchmarks.get("optimized", {})
                        
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        
                        with metric_col1:
                            st.metric(
                                "Speedup Factor",
                                f"{speedup}x",
                                f"+{((speedup - 1) * 100):.1f}%"
                            )
                        
                        with metric_col2:
                            time_saved = orig_bench.get("runtime_ms", 0) - opt_bench.get("runtime_ms", 0)
                            st.metric(
                                "Time Saved",
                                f"{time_saved:.2f} ms",
                                f"-{(time_saved / orig_bench.get('runtime_ms', 1) * 100):.1f}%"
                            )
                        
                        with metric_col3:
                            mem_saved = orig_bench.get("memory_mb", 0) - opt_bench.get("memory_mb", 0)
                            st.metric(
                                "Memory Saved",
                                f"{mem_saved:.2f} MB",
                                f"-{(mem_saved / orig_bench.get('memory_mb', 1) * 100):.1f}%" if orig_bench.get('memory_mb', 0) > 0 else "0%"
                            )
                    
                    # AI Explanation
                    ai_explanation = result.get("ai_explanation")
                    if ai_explanation:
                        st.markdown("### 💡 AI Explanation")
                        st.info(ai_explanation)
                    
                    # Safety analysis
                    safety = result.get("safety_analysis", {})
                    if safety:
                        st.markdown("### 🛡️ Safety Analysis")
                        if safety.get("is_safe", True):
                            st.success("✅ All safety checks passed")
                        else:
                            st.warning("⚠️ Safety warnings detected:")
                            for warning in safety.get("warnings", []):
                                st.markdown(f"- {warning}")
                
                with tab2:
                    # Code comparison
                    st.markdown("### 📝 Code Comparison")
                    
                    comp_col1, comp_col2 = st.columns(2)
                    
                    with comp_col1:
                        st.markdown("**Original Code**")
                        st.code(result.get("original_code", ""), language="python")
                    
                    with comp_col2:
                        st.markdown("**Optimized Code**")
                        optimized_code = result.get("optimized_code", "")
                        st.code(optimized_code, language="python")
                    
                    # Rules detected
                    rules = result.get("rules_detected", [])
                    if rules:
                        st.markdown("### 🔍 Optimizations Applied")
                        for i, rule in enumerate(rules, 1):
                            with st.expander(f"Rule {i}: {rule.get('message', 'Optimization')}"):
                                st.markdown(f"**Suggestion:** {rule.get('suggestion', 'N/A')}")
                                st.markdown(f"**Severity:** {rule.get('severity', 'medium')}")
                                st.markdown(f"**Line:** {rule.get('line', 'N/A')}")
                
                with tab3:
                    # Download options
                    st.markdown("### 💾 Download Optimized Code")
                    
                    optimized_code = result.get("optimized_code", "")
                    
                    # Generate new filename
                    original_name = uploaded_file.name.replace(".py", "")
                    optimized_filename = f"{original_name}_optimized.py"
                    
                    st.download_button(
                        "⬇️ Download Optimized File",
                        optimized_code,
                        file_name=optimized_filename,
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    # Auto download
                    if auto_download:
                        st.info(f"📥 File ready: {optimized_filename}")
                    
                    # Add to history
                    if "history" not in st.session_state:
                        st.session_state.history = []
                    
                    history_entry = {
                        "Job ID": f"CF-{datetime.now().strftime('%Y%m%d')}-{file_hash}",
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Mode": result.get("mode", "UNKNOWN"),
                        "Speedup": f"{speedup}x" if benchmarks else "N/A",
                        "Status": "✅ Success",
                        "File": uploaded_file.name
                    }
                    
                    if history_entry not in st.session_state.history:
                        st.session_state.history.insert(0, history_entry)
                    
                    st.success("✅ Added to optimization history")
            
            else:
                st.error(f"❌ Optimization failed: {result.get('message', 'Unknown error')}")
    
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")

else:
    # No file uploaded - show upload area
    st.markdown("""
    <div class='upload-area'>
        <h3>📁 Drop your Python file here</h3>
        <p>or click above to browse</p>
        <br>
        <p style='color:#9ca3af; font-size:14px;'>
            Supported: .py files only<br>
            Maximum size: 10,000 characters
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick tips
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    - **Single files only**: Upload one .py file at a time
    - **Clean code**: Remove debug prints and unnecessary comments
    - **Test locally first**: Make sure your code runs before uploading
    - **Backup**: Keep a copy of your original code
    - **Review results**: Always review optimized code before using in production
    """)

st.markdown("---")
st.caption("© 2025 CodeForge | Secure File Upload")
