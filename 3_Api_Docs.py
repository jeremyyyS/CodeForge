import streamlit as st
from utils.auth import require_auth, get_current_user
import json

require_auth()

st.set_page_config(page_title="API Docs", page_icon="📄", layout="wide")

# Styling
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.endpoint-card {
    background:#0f1729;
    border-left:4px solid #3b82f6;
    border-radius:8px;
    padding:16px;
    margin:12px 0;
}
.method-badge {
    display:inline-block;
    padding:4px 10px;
    border-radius:4px;
    font-weight:600;
    font-size:12px;
    margin-right:8px;
}
.method-post {background:#10b981; color:white;}
.method-get {background:#3b82f6; color:white;}
code {
    background:#1e293b;
    padding:2px 6px;
    border-radius:4px;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

user = get_current_user()

# Header
col1, col2 = st.columns([8, 2])
with col1:
    st.title("📄 API Documentation")
    st.caption("Complete guide to CodeForge backend endpoints")
with col2:
    st.write(f"👤 **{user['username']}**")

st.markdown("---")

# Base URL
st.markdown("### 🔗 Base URL")
st.code("http://localhost:8000", language="text")
st.caption("Make sure the FastAPI backend is running on this port")

st.markdown("---")

# Tabs for organization
tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 Main Endpoints",
    "📦 Request/Response",
    "🧪 Try It Out",
    "💡 Examples"
])

# TAB 1: Main Endpoints
with tab1:
    st.markdown("## Available Endpoints")
    
    # Health Check
    st.markdown("""
    <div class='endpoint-card'>
        <span class='method-badge method-get'>GET</span>
        <strong>/</strong>
        <p>Health check endpoint to verify backend is running</p>
        <p><strong>Response:</strong></p>
        <pre><code>{
  "message": "SafeOpt Code Optimizer",
  "status": "running",
  "version": "1.0"
}</code></pre>
    </div>
    """, unsafe_allow_html=True)
    
    # Optimize (Hybrid)
    st.markdown("""
    <div class='endpoint-card'>
        <span class='method-badge method-post'>POST</span>
        <strong>/optimize</strong>
        <p>🤖 AI-powered hybrid optimization (rules + Gemini AI)</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>Rule-based pattern detection</li>
            <li>Semantic pattern analysis</li>
            <li>AI-generated optimizations</li>
            <li>Performance benchmarking</li>
            <li>Safety validation</li>
            <li>Confidence scoring</li>
            <li>AI explanations</li>
        </ul>
        <p><strong>Request Body:</strong></p>
        <pre><code>{
  "code": "def fibonacci(n):\\n    if n <= 1:\\n        return n\\n    return fibonacci(n-1) + fibonacci(n-2)"
}</code></pre>
        <p><strong>Response includes:</strong> optimized_code, rules_detected, benchmarks, safety_analysis, confidence, explainability, ai_explanation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Optimize Rules Only (Full)
    st.markdown("""
    <div class='endpoint-card'>
        <span class='method-badge method-post'>POST</span>
        <strong>/optimize-rules-only</strong>
        <p>⚡ Fast rule-based optimization with full benchmarking</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>AST-based rule detection</li>
            <li>Deterministic transformations</li>
            <li>Performance benchmarks</li>
            <li>No AI/API calls (offline)</li>
        </ul>
        <p><strong>Response includes:</strong> optimized_code, rules_detected, transformations, benchmarks (original, optimized, speedup)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Optimize Rules Only (Simple)
    st.markdown("""
    <div class='endpoint-card'>
        <span class='method-badge method-post'>POST</span>
        <strong>/optimize-rules-only/simple</strong>
        <p>⚡ Lightweight rule-based optimization (no benchmarking)</p>
        <p><strong>Use case:</strong> Quick optimizations when you don't need performance metrics</p>
        <p><strong>Response:</strong> Just original_code and optimized_code</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload File
    st.markdown("""
    <div class='endpoint-card'>
        <span class='method-badge method-post'>POST</span>
        <strong>/upload</strong>
        <p>📂 Upload a .py file for optimization</p>
        <p><strong>Content-Type:</strong> multipart/form-data</p>
        <p><strong>File Requirements:</strong></p>
        <ul>
            <li>Must be a .py file</li>
            <li>Max 10,000 characters</li>
        </ul>
        <p><strong>Note:</strong> Automatically uses hybrid optimization</p>
    </div>
    """, unsafe_allow_html=True)

# TAB 2: Request/Response Schemas
with tab2:
    st.markdown("## 📦 Request/Response Schemas")
    
    st.markdown("### Request Schema")
    request_schema = {
        "code": {
            "type": "string",
            "min_length": 1,
            "max_length": 10000,
            "description": "Python code to optimize"
        }
    }
    st.json(request_schema)
    
    st.markdown("---")
    
    st.markdown("### Response Schema (Hybrid /optimize)")
    response_schema = {
        "mode": "HYBRID",
        "status": "success",
        "original_code": "string",
        "optimized_code": "string",
        "rules_detected": [
            {
                "message": "Issue description",
                "suggestion": "How to fix",
                "line": "number",
                "severity": "high|medium|low"
            }
        ],
        "benchmarks": {
            "original": {
                "runtime_ms": "number",
                "memory_mb": "number",
                "variance_pct": "number"
            },
            "optimized": {
                "runtime_ms": "number",
                "memory_mb": "number"
            },
            "speedup_factor": "number"
        },
        "safety_analysis": {
            "is_safe": "boolean",
            "warnings": ["string"],
            "code_growth_factor": "number",
            "complexity_change": "number"
        },
        "confidence": {
            "score": "number (0-100)",
            "level": "high|medium|low",
            "factors": {}
        },
        "explainability": {
            "summary": "string",
            "changes": ["string"]
        },
        "ai_explanation": "string",
        "timestamp": "ISO 8601 datetime"
    }
    st.json(response_schema)

# TAB 3: Try It Out
with tab3:
    st.markdown("## 🧪 Test the API")
    
    # Endpoint selector
    endpoint = st.selectbox(
        "Select Endpoint:",
        [
            "GET /",
            "POST /optimize",
            "POST /optimize-rules-only",
            "POST /optimize-rules-only/simple"
        ]
    )
    
    if endpoint == "GET /":
        if st.button("Send Request", type="primary"):
            from utils import api
            result = api.api_client.health_check()
            st.json(result)
    
    else:
        # Code input for POST endpoints
        test_code = st.text_area(
            "Python Code:",
            value="def sum_list(lst):\n    total = 0\n    for num in lst:\n        total += num\n    return total",
            height=150
        )
        
        if st.button("Send Request", type="primary"):
            from utils import api
            
            with st.spinner("Sending request..."):
                if endpoint == "POST /optimize":
                    result = api.optimize(test_code)
                elif endpoint == "POST /optimize-rules-only":
                    result = api.benchmark_only(test_code)
                else:  # simple
                    result = api.optimize_simple(test_code)
            
            st.markdown("### Response:")
            st.json(result)

# TAB 4: Code Examples
with tab4:
    st.markdown("## 💡 Code Examples")
    
    # Python example
    st.markdown("### Python (using requests)")
    st.code("""
import requests

# Hybrid optimization
response = requests.post(
    "http://localhost:8000/optimize",
    json={"code": "def fib(n):\\n    if n<=1: return n\\n    return fib(n-1)+fib(n-2)"},
    timeout=90
)

result = response.json()
print(result["optimized_code"])
print(f"Speedup: {result['benchmarks']['speedup_factor']}x")
print(f"AI Explanation: {result['ai_explanation']}")
    """, language="python")
    
    st.markdown("---")
    
    # cURL example
    st.markdown("### cURL")
    st.code("""
curl -X POST "http://localhost:8000/optimize" \\
  -H "Content-Type: application/json" \\
  -d '{
    "code": "def fibonacci(n):\\n    if n <= 1:\\n        return n\\n    return fibonacci(n-1) + fibonacci(n-2)"
  }'
    """, language="bash")
    
    st.markdown("---")
    
    # JavaScript example
    st.markdown("### JavaScript (fetch)")
    st.code("""
const optimizeCode = async (code) => {
  const response = await fetch('http://localhost:8000/optimize', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ code })
  });
  
  const result = await response.json();
  console.log('Optimized:', result.optimized_code);
  console.log('Speedup:', result.benchmarks.speedup_factor + 'x');
  console.log('AI Explanation:', result.ai_explanation);
  return result;
};

optimizeCode(`
def sum_numbers(n):
    total = 0
    for i in range(n):
        total += i
    return total
`);
    """, language="javascript")

st.markdown("---")
st.markdown("### 📚 Additional Resources")
st.markdown("""
- **Backend Source**: `jeremy_final.py`
- **Config**: `config.py`
- **API Framework**: FastAPI
- **AI Model**: Gemini 2.5 Flash
- **Default Port**: 8000

For issues or questions, contact your system administrator.
""")

st.caption("© 2025 CodeForge | API Documentation")
