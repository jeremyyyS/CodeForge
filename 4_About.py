import streamlit as st
from utils.auth import require_auth, get_current_user

require_auth()

st.set_page_config(page_title="About CodeForge", page_icon="ℹ️", layout="wide")

# Styling
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.feature-card {
    background:#0f1729;
    border:1px solid #1f2937;
    border-radius:10px;
    padding:20px;
    margin:12px 0;
}
.tech-badge {
    display:inline-block;
    background:#1e293b;
    border:1px solid #334155;
    padding:6px 12px;
    border-radius:6px;
    margin:4px;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

user = get_current_user()

# Header
col1, col2 = st.columns([8, 2])
with col1:
    st.title("ℹ️ About CodeForge")
    st.caption("AI-Powered Code Optimization Platform")
with col2:
    st.write(f"👤 **{user['username']}**")

st.markdown("---")

# Project Overview
st.markdown("""
### 🧩 What is CodeForge?

CodeForge is an **AI-powered code optimization platform** that automatically transforms
unoptimized Python code into efficient, high-performance versions using a combination of:

- **Rule-Based Analysis**: AST parsing and pattern detection
- **Semantic Understanding**: Deep code comprehension
- **AI Optimization**: Gemini 2.5 Flash for intelligent code rewriting
- **Safety Validation**: Ensuring optimizations don't break functionality
- **Performance Benchmarking**: Real-time measurement of improvements
""")

st.markdown("---")

# Key Features
st.markdown("### ⚙️ Key Features")

col_f1, col_f2 = st.columns(2)

with col_f1:
    st.markdown("""
    <div class='feature-card'>
        <h4>🤖 Hybrid Optimization</h4>
        <p>Combines rule-based transformations with AI-powered optimization for best results</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-card'>
        <h4>📊 Real-Time Benchmarking</h4>
        <p>Measures runtime, memory usage, and speedup factors with statistical accuracy</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-card'>
        <h4>🔍 Deep Code Analysis</h4>
        <p>Detects inefficient patterns, nested loops, recursion issues, and more</p>
    </div>
    """, unsafe_allow_html=True)

with col_f2:
    st.markdown("""
    <div class='feature-card'>
        <h4>🛡️ Safety Guarantees</h4>
        <p>Validates optimizations don't introduce bugs or change program behavior</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-card'>
        <h4>💡 AI Explanations</h4>
        <p>Natural language explanations of why optimizations improve performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-card'>
        <h4>📈 Confidence Scoring</h4>
        <p>Transparent metrics about optimization quality and reliability</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Technology Stack
st.markdown("### 🛠 Technology Stack")

st.markdown("#### Backend")
tech_backend = [
    "Python 3.x",
    "FastAPI",
    "Google Gemini 2.5 Flash",
    "AST (Abstract Syntax Trees)",
    "Asyncio",
    "Pydantic"
]
for tech in tech_backend:
    st.markdown(f"<span class='tech-badge'>{tech}</span>", unsafe_allow_html=True)

st.markdown("#### Frontend")
tech_frontend = [
    "Streamlit",
    "Plotly",
    "Pandas",
    "Requests"
]
for tech in tech_frontend:
    st.markdown(f"<span class='tech-badge'>{tech}</span>", unsafe_allow_html=True)

st.markdown("---")

# How It Works
st.markdown("### 🔄 How It Works")

st.markdown("""
#### Optimization Pipeline

1. **Code Analysis** 📝
   - Parse code into Abstract Syntax Tree (AST)
   - Detect patterns and anti-patterns
   - Identify optimization opportunities

2. **Rule Application** ⚡
   - Apply deterministic transformation rules
   - Convert inefficient patterns to efficient ones
   - Preserve code semantics

3. **Semantic Analysis** 🔍
   - Deep understanding of code intent
   - Context-aware optimization suggestions
   - Pattern detection beyond syntax

4. **AI Enhancement** 🤖
   - Gemini AI generates optimized version
   - Considers rules and semantic patterns
   - Creates human-readable, idiomatic code

5. **Safety Validation** 🛡️
   - Verify syntax correctness
   - Check for code bloat
   - Measure complexity changes
   - Detect potential issues

6. **Benchmarking** 📊
   - Measure original vs optimized runtime
   - Track memory usage
   - Calculate speedup factors
   - Statistical variance analysis

7. **Explanation Generation** 💡
   - AI explains the optimizations
   - Technical details about improvements
   - Confidence scoring
""")

st.markdown("---")

# Academic Context
st.markdown("### 🎓 Academic Project")

st.markdown("""
This project is part of our **Final Year Project** for the:

**Department of Artificial Intelligence & Data Science**  
Rajagiri School of Engineering & Technology

**Project Team:**
- AI/DS Final Year Students
- Guided by Faculty Advisors

**Research Focus:**
- Automated code optimization using hybrid AI approaches
- Performance analysis and benchmarking methodologies
- Safety-aware program transformation
- Explainable AI in software engineering
""")

st.markdown("---")

# Vision & Future Work
st.markdown("### 💡 Vision")

st.markdown("""
> To make performance optimization **accessible to every developer** —
> no compiler theory or manual refactoring required.

**Future Enhancements:**
- Multi-language support (JavaScript, Java, C++)
- IDE integrations (VS Code, PyCharm)
- Custom optimization rules
- Team collaboration features
- Advanced ML models for optimization
- Cloud deployment
- Batch processing for large codebases
""")

st.markdown("---")

# System Info
st.markdown("### 📋 System Information")

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown("""
    **Version**  
    1.0.0 (Beta)
    """)

with info_col2:
    st.markdown("""
    **Last Updated**  
    February 2025
    """)

with info_col3:
    st.markdown("""
    **License**  
    Academic Project
    """)

# Contact
st.markdown("---")
st.markdown("### 📧 Contact & Support")
st.markdown("""
For questions, bug reports, or feature requests:

- **GitHub**: [github.com/jeremyyyS/CodeForge](https://github.com/jeremyyyS/CodeForge)
- **Email**: Contact through university portal
- **Documentation**: See API Docs page

**Acknowledgments:**
- Rajagiri School of Engineering & Technology
- Department of AI & Data Science
- Google Gemini AI Team
- Open Source Community
""")

st.markdown("---")
st.caption("© 2025 CodeForge | Built with ❤️ for better code")
