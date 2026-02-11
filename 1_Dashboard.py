import os
import hashlib
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.auth import require_auth, get_current_user
from utils import api

# 🔐 Auth guard
require_auth()
user = get_current_user()

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="CodeForge – Optimize Python",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ Helpers ------------------
def load_example() -> str:
    try:
        with open("assets/examples/fib_unoptimized.py", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "print('hello world')"

def code_hash(code: str) -> str:
    return hashlib.sha1(code.encode("utf-8")).hexdigest()[:8]

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ Sidebar ------------------
st.sidebar.title("TOOLS")

uploaded = st.sidebar.file_uploader(
    "📂 Upload Code File (.py)",
    type=["py"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset Tools**")
st.sidebar.caption("Curate optimization datasets and run validations.")

st.sidebar.markdown("---")
st.sidebar.markdown("**🔑 Admin Login**")
st.sidebar.caption("Protected dataset & model operations.")

# ------------------ Top Nav ------------------
st.markdown("""
<style>
#MainMenu, header, footer {visibility:hidden;}
.topnav {
  background:#0d1b2a; padding:10px 16px; border-bottom:1px solid #1f2937;
  display:flex; justify-content:space-between; align-items:center;
}
.topnav a {
  color:#d1d5db; margin-right:20px; text-decoration:none; font-weight:500;
}
.topnav a:hover { color:#fff; }
.search {
  padding:8px 10px; border-radius:8px;
  background:#0b1220; border:1px solid #374151;
  color:#e5e7eb; min-width:340px;
}
.metric-card {
  border:1px solid #1f2937;
  border-radius:14px;
  padding:14px 16px;
  background:#0b1220;
}
</style>

<div class="topnav">
  <div>
    <a>Home</a>
    <a>History</a>
    <a>API Docs</a>
    <a>About</a>
  </div>
  <input class="search" placeholder="Search docs, code, or jobs..." />
</div>
""", unsafe_allow_html=True)

# ------------------ Header ------------------
st.title("⚙️ CodeForge")
st.caption("Shaping smarter, faster, leaner code")

st.write(f"👤 **{user['username']}**")

# ------------------ Code Panels ------------------
colL, colR = st.columns([1, 1], gap="large")

with colL:
    st.subheader("Unoptimized Python Code")

    default_text = load_example()
    if uploaded:
        default_text = uploaded.read().decode("utf-8")

    code_in = st.text_area(
        "Paste your Python code here",
        value=default_text,
        height=280,
        label_visibility="collapsed"
    )

    c1, c2, c3 = st.columns([0.4, 0.3, 0.3])
    run = c1.button("🚀 Optimize Code", type="primary", use_container_width=True)
    bench = c2.button("📊 Benchmark Only", use_container_width=True)
    clear = c3.button("🧹 Clear", use_container_width=True)

with colR:
    st.subheader("AI-Optimized Code")
    optimized_placeholder = st.empty()

# ------------------ Actions ------------------
metrics = {}
status = None
message = None
result = None

if clear:
    st.session_state.history = []
    st.rerun()

if run and code_in.strip():
    with st.spinner("Optimizing…"):
        result = api.api_client.optimize(code_in)

    status = result.get("status", "ERROR")
    metrics = result.get("benchmarks", {}) or {}

    if status != "SUCCESS":
        st.error("Optimization failed.")
    else:
        optimized_placeholder.code(
            result.get("optimized_code", "# (no output)"),
            language="python"
        )

elif bench and code_in.strip():
    with st.spinner("Benchmarking…"):
        result = api.api_client.optimize_rules_only(code_in)

    status = result.get("status", "ERROR")
    metrics = result.get("benchmarks", {}) or {}

    if status != "SUCCESS":
        st.error("Benchmark failed.")

# ------------------ Metrics ------------------
st.markdown("### Performance Metrics")

orig = metrics.get("original", {})
opt = metrics.get("optimized", {})

orig_ms = orig.get("runtime_ms")
opt_ms = opt.get("runtime_ms")
speed = metrics.get("speedup_factor")

orig_mem = orig.get("memory_mb")
opt_mem = opt.get("memory_mb")

m1, m2, m3 = st.columns(3)

with m1:
    val = f"{round(orig_ms - opt_ms, 2)} ms" if orig_ms and opt_ms else "—"
    st.markdown(
        f"<div class='metric-card'><b>Runtime Saved</b><br>{val}</div>",
        unsafe_allow_html=True
    )

with m2:
    val = f"{round(orig_mem - opt_mem, 2)} MB" if orig_mem and opt_mem else "—"
    st.markdown(
        f"<div class='metric-card'><b>Memory Reduction</b><br>{val}</div>",
        unsafe_allow_html=True
    )

with m3:
    val = f"×{round(speed, 2)}" if speed else "—"
    st.markdown(
        f"<div class='metric-card'><b>Speedup Factor</b><br>{val}</div>",
        unsafe_allow_html=True
    )

# ------------------ Charts ------------------
st.markdown("### Runtime Comparison & Memory Usage")

cA, cB = st.columns(2)

if orig_ms is not None:
    df = pd.DataFrame({
        "Type": ["Before", "After"],
        "Time": [orig_ms, opt_ms or orig_ms]
    })
    fig = px.bar(df, x="Type", y="Time", title="Runtime (ms)", text="Time")
    cA.plotly_chart(fig, use_container_width=True)
else:
    cA.info("Run optimization to see runtime comparison.")

if orig_mem is not None:
    df = pd.DataFrame({
        "Type": ["Before", "After"],
        "Memory": [orig_mem, opt_mem or orig_mem]
    })
    fig = px.bar(df, x="Type", y="Memory", title="Memory (MB)", text="Memory")
    cB.plotly_chart(fig, use_container_width=True)
else:
    cB.info("Memory metrics will appear when backend returns them.")

# ------------------ AI Explanation ------------------
if result and result.get("ai_explanation"):
    st.markdown("### 🧠 AI Explanation")
    st.info(result["ai_explanation"])

# ------------------ Safety & Confidence ------------------
if result and result.get("confidence"):
    st.markdown("### 🛡 Confidence & Safety")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Confidence", f"{result['confidence']['overall']}%")
        st.write("Level:", result["confidence"]["confidence_level"])
    with c2:
        st.write("Recommendation:", result["confidence"]["recommendation"])
        st.write("Safety:", result["safety_analysis"]["verdict"])

# ------------------ Rules Applied ------------------
if result and result.get("rules_detected"):
    st.markdown("### 🔍 Optimizations Applied")
    for r in result["rules_detected"]:
        st.markdown(f"- **{r['message']}** → {r['suggestion']}")

# ------------------ History ------------------
if status == "SUCCESS" and code_in.strip():
    st.session_state.history.insert(0, {
        "Job ID": result.get("job_id"),
        "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
        "Mode": result.get("mode"),
        "Speedup": f"{round(speed, 2)}x" if speed else "—",
        "Status": "✅ Success"
    })

st.markdown("### Previous Submissions")

if st.session_state.history:
    st.dataframe(
        pd.DataFrame(st.session_state.history[:10]),
        use_container_width=True
    )
else:
    st.caption("No previous submissions yet.")

st.markdown("---")
st.caption("© CodeForge – Frontend prototype")
