import streamlit as st

st.set_page_config(page_title="Optimization Report", layout="wide")
st.title("📄 Optimization Report")

data = st.session_state.get("last_result")
if not data:
    st.warning("No optimization data available.")
    st.stop()

st.subheader("Optimized Code")
st.code(data["optimized_code"], language="python")

st.subheader("AI Explanation")
st.info(data["ai_explanation"])

st.subheader("Rules Applied")
for r in data.get("rules", []):
    st.write(f"- {r['message']} → {r['suggestion']}")

st.subheader("Confidence")
st.write(data["confidence"])

st.subheader("Safety Analysis")
st.write(data["safety"])
