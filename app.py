import streamlit as st

# App entry router
if st.session_state.get("auth", {}).get("is_auth"):
    st.switch_page("pages/1_Dashboard.py")
else:
    st.switch_page("pages/0_Login.py")
