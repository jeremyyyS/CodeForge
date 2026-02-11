import streamlit as st
import pandas as pd
import io
from utils.auth import require_auth, get_current_user

require_auth()

st.set_page_config(page_title="Dataset Tools", page_icon="🗃", layout="wide")

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
.dataset-card {
    background:#0f1729;
    border:1px solid #1f2937;
    border-radius:10px;
    padding:16px;
    margin:12px 0;
}
.stat-box {
    background:#1e293b;
    padding:16px;
    border-radius:8px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

user = get_current_user()

# Admin check
if user.get("role") != "admin":
    st.error("🚫 Access Denied")
    st.warning("This page is only accessible to administrators.")
    st.stop()

# Header
st.markdown("<div class='admin-banner'>🔑 ADMIN AREA</div>", unsafe_allow_html=True)

col1, col2 = st.columns([8, 2])
with col1:
    st.title("🗃 Dataset Tools")
    st.caption("Manage training and benchmark datasets for CodeForge")
with col2:
    st.write(f"👤 **{user['username']}**")
    st.caption(f"Role: `{user['role']}`")

st.markdown("---")

# Tab organization
tab1, tab2, tab3, tab4 = st.tabs([
    "📤 Upload Dataset",
    "📊 View Datasets",
    "✅ Validation",
    "📚 Documentation"
])

# TAB 1: Upload Dataset
with tab1:
    st.markdown("### 📤 Upload New Dataset")
    
    st.markdown("""
    Upload CSV files containing code optimization pairs for:
    - **Training data**: Used to improve the optimization model
    - **Benchmark data**: Used to evaluate performance
    - **Test cases**: Used for validation
    """)
    
    dataset_type = st.selectbox(
        "Dataset Type:",
        ["Training", "Benchmark", "Test Cases", "Other"]
    )
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="CSV file with unoptimized and optimized code pairs"
    )
    
    if uploaded_file:
        try:
            # Read CSV
            content = uploaded_file.getvalue().decode("utf-8")
            df = pd.read_csv(io.StringIO(content))
            
            st.success(f"✅ File uploaded: **{uploaded_file.name}**")
            
            # Display info
            info_col1, info_col2, info_col3 = st.columns(3)
            with info_col1:
                st.metric("Total Rows", len(df))
            with info_col2:
                st.metric("Columns", len(df.columns))
            with info_col3:
                file_size_kb = len(content) / 1024
                st.metric("File Size", f"{file_size_kb:.2f} KB")
            
            # Preview
            st.markdown("#### 👀 Dataset Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Save dataset
            if st.button("💾 Save Dataset", type="primary"):
                # In production, save to database or file system
                st.success("✅ Dataset saved successfully!")
                st.info(f"📁 Saved as: {dataset_type.lower()}/{uploaded_file.name}")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

# TAB 2: View Datasets
with tab2:
    st.markdown("### 📊 Existing Datasets")
    
    # Mock data - replace with actual database queries in production
    datasets = [
        {
            "Name": "python_optimizations_v1.csv",
            "Type": "Training",
            "Rows": 1500,
            "Last Updated": "2025-02-01",
            "Status": "✅ Active"
        },
        {
            "Name": "benchmark_suite.csv",
            "Type": "Benchmark",
            "Rows": 300,
            "Last Updated": "2025-01-28",
            "Status": "✅ Active"
        },
        {
            "Name": "test_cases_v2.csv",
            "Type": "Test Cases",
            "Rows": 200,
            "Last Updated": "2025-01-25",
            "Status": "🔄 Pending"
        }
    ]
    
    if datasets:
        df_datasets = pd.DataFrame(datasets)
        st.dataframe(
            df_datasets,
            use_container_width=True,
            column_config={
                "Status": st.column_config.TextColumn("Status")
            }
        )
        
        # Actions
        st.markdown("---")
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        with action_col2:
            if st.button("📥 Export All", use_container_width=True):
                st.info("Export functionality coming soon")
        
        with action_col3:
            if st.button("🗑 Clean Up", use_container_width=True):
                st.warning("This will remove inactive datasets")
    else:
        st.info("No datasets found. Upload your first dataset above.")

# TAB 3: Validation
with tab3:
    st.markdown("### ✅ Dataset Validation")
    
    st.markdown("""
    Validate uploaded datasets to ensure they meet quality standards:
    """)
    
    if uploaded_file and 'df' in locals():
        st.markdown("#### 🔍 Validation Results")
        
        # Required columns check
        required_cols = ["unoptimized_code", "optimized_code"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        validation_results = []
        
        # Check 1: Required columns
        if missing_cols:
            validation_results.append({
                "Check": "Required Columns",
                "Status": "❌ Failed",
                "Details": f"Missing: {', '.join(missing_cols)}"
            })
        else:
            validation_results.append({
                "Check": "Required Columns",
                "Status": "✅ Passed",
                "Details": "All required columns present"
            })
        
        # Check 2: Empty values
        empty_count = df[required_cols].isnull().sum().sum()
        if empty_count > 0:
            validation_results.append({
                "Check": "Empty Values",
                "Status": "⚠️ Warning",
                "Details": f"{empty_count} empty cells found"
            })
        else:
            validation_results.append({
                "Check": "Empty Values",
                "Status": "✅ Passed",
                "Details": "No empty values"
            })
        
        # Check 3: Code syntax
        syntax_errors = 0
        for idx, row in df.head(10).iterrows():  # Check first 10 for performance
            try:
                compile(row.get('unoptimized_code', ''), '<string>', 'exec')
                compile(row.get('optimized_code', ''), '<string>', 'exec')
            except SyntaxError:
                syntax_errors += 1
        
        if syntax_errors > 0:
            validation_results.append({
                "Check": "Code Syntax",
                "Status": "❌ Failed",
                "Details": f"{syntax_errors}/10 samples have syntax errors"
            })
        else:
            validation_results.append({
                "Check": "Code Syntax",
                "Status": "✅ Passed",
                "Details": "All samples syntactically valid"
            })
        
        # Display results
        df_validation = pd.DataFrame(validation_results)
        st.dataframe(df_validation, use_container_width=True, hide_index=True)
        
        # Statistics
        st.markdown("#### 📊 Dataset Statistics")
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.markdown("<div class='stat-box'><strong>Total Pairs</strong><br>" + 
                       f"{len(df)}</div>", unsafe_allow_html=True)
        
        with stat_col2:
            avg_orig_len = df['unoptimized_code'].str.len().mean() if 'unoptimized_code' in df else 0
            st.markdown("<div class='stat-box'><strong>Avg Original Length</strong><br>" + 
                       f"{int(avg_orig_len)} chars</div>", unsafe_allow_html=True)
        
        with stat_col3:
            avg_opt_len = df['optimized_code'].str.len().mean() if 'optimized_code' in df else 0
            st.markdown("<div class='stat-box'><strong>Avg Optimized Length</strong><br>" + 
                       f"{int(avg_opt_len)} chars</div>", unsafe_allow_html=True)
        
        with stat_col4:
            if 'runtime_improvement' in df.columns:
                avg_improvement = df['runtime_improvement'].mean()
                st.markdown("<div class='stat-box'><strong>Avg Improvement</strong><br>" + 
                           f"{avg_improvement:.1f}%</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='stat-box'><strong>Avg Improvement</strong><br>N/A</div>", 
                           unsafe_allow_html=True)
    
    else:
        st.info("Upload a dataset in the Upload tab to validate it")

# TAB 4: Documentation
with tab4:
    st.markdown("### 📚 Dataset Format Documentation")
    
    st.markdown("""
    #### Required CSV Format
    
    Your dataset CSV file must include these columns:
    
    | Column Name | Type | Required | Description |
    |------------|------|----------|-------------|
    | `unoptimized_code` | string | ✅ Yes | Original inefficient Python code |
    | `optimized_code` | string | ✅ Yes | Optimized version of the code |
    | `runtime_improvement` | float | ❌ No | Percentage runtime improvement |
    | `memory_reduction` | float | ❌ No | Percentage memory reduction |
    | `test_case_passed` | boolean | ❌ No | Whether optimization passes tests |
    | `complexity_before` | string | ❌ No | Big-O complexity before (e.g., "O(n²)") |
    | `complexity_after` | string | ❌ No | Big-O complexity after |
    | `category` | string | ❌ No | Type of optimization (loop, recursion, etc.) |
    | `description` | string | ❌ No | Human-readable description |
    
    #### Example CSV Content
    """)
    
    example_csv = """unoptimized_code,optimized_code,runtime_improvement,category
"def sum_list(lst):
    total = 0
    for num in lst:
        total += num
    return total","def sum_list(lst):
    return sum(lst)",45.2,builtin_usage
"def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)","def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a",98.5,recursion_to_iteration"""
    
    st.code(example_csv, language="csv")
    
    st.markdown("---")
    
    st.markdown("""
    #### Best Practices
    
    1. **Code Quality**
       - Ensure all code snippets are syntactically valid
       - Include diverse optimization patterns
       - Test optimized versions maintain functionality
    
    2. **Metadata**
       - Include performance metrics when available
       - Document complexity changes
       - Categorize optimizations for analysis
    
    3. **Size**
       - Keep individual code snippets under 500 lines
       - Aim for 100+ examples per category
       - Balance simple and complex optimizations
    
    4. **Validation**
       - Always validate datasets before using for training
       - Check for duplicate entries
       - Verify optimization claims with benchmarks
    """)

st.markdown("---")
st.caption("© 2025 CodeForge | Admin Dataset Tools")
