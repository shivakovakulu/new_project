import streamlit as st
from auth.session import init_session, check_session_timeout
from utils.helpers import inject_custom_css

# Page Configuration - Must be the first streamlit call
st.set_page_config(
    page_title="SmartCampusAI - Entrypoint",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Initialize session variables
init_session()

# 2. Check for inactivity timeout
check_session_timeout()

# 3. Inject Glassmorphism Design Styles
inject_custom_css()

# 4. Programmatic routing based on authentication
if st.session_state.authenticated:
    st.switch_page("pages/Dashboard.py")
else:
    st.switch_page("pages/Login.py")
