import streamlit as st
from auth.session import require_guest
from auth.authentication import login_user
from utils.helpers import inject_custom_css, load_lottie_url
from streamlit_lottie import st_lottie
import os

# Page configuration
st.set_page_config(
    page_title="SmartCampusAI - Login",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. Enforce guest status (redirects logged in users to Dashboard)
require_guest()

# 2. Inject custom CSS and background image styling
inject_custom_css()

# Hide default sidebar toggle for the login screen
st.markdown("""
<style>
[data-testid="collapsedControl"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# 3. UI Layout
col1, col2 = st.columns([1.3, 1], gap="large")

with col1:
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # Custom logo and title display
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
        
    st.markdown("""
    <h1 style='font-size: 56px; font-weight: 800; margin-top: 15px; margin-bottom: 5px; background: linear-gradient(135deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        SmartCampusAI
    </h1>
    <h3 style='color: #e5e7eb; font-weight: 500; font-size: 22px; margin-top: 0;'>
        The next-generation intelligence layer for modern campuses.
    </h3>
    <p style='color: #9ca3af; font-size: 15px; line-height: 1.6; max-width: 500px;'>
        Log in to access your administrative tools, AI assistant panel, real-time campus data metrics, and account profile controls.
    </p>
    """, unsafe_allow_html=True)
    
    # Load Lottie Animation
    lottie_url = "https://lottie.host/8c6426db-19a9-4674-8848-d3e9185a953e/2jVjQYk61M.json" # Tech animation
    lottie_json = load_lottie_url(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, height=350, key="login_anim")
    else:
        st.markdown("<div style='height: 350px;'></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
    
    # Login form inside a glassmorphic container
    with st.container(border=True):
        st.markdown("""
        <h2 style='text-align: center; color: #f3f4f6; font-weight: 700; margin-top: 0; margin-bottom: 25px;'>
            Account Login
        </h2>
        """, unsafe_allow_html=True)
        
        username_or_email = st.text_input(
            "Username or Email", 
            placeholder="Enter username or email address", 
            key="login_username"
        )
        
        password = st.text_input(
            "Password", 
            type="password", 
            placeholder="Enter password", 
            key="login_password"
        )
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        if st.button("Access Dashboard", key="login_submit_btn"):
            if not username_or_email or not password:
                st.error("Please enter both your credentials.")
            else:
                result = login_user(username_or_email, password)
                if result["success"]:
                    st.success(result["message"])
                    # Redirect to dashboard
                    st.switch_page("pages/Dashboard.py")
                else:
                    st.error(result["message"])
                    
        st.markdown("""
        <hr style='border-color: rgba(255, 255, 255, 0.08); margin: 25px 0 15px 0;' />
        <div style='text-align: center; color: #9ca3af; font-size: 13px; margin-bottom: 12px;'>
            New to SmartCampusAI?
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("Create Student / Staff Account", key="login_register_nav"):
            st.switch_page("pages/Register.py")
        st.markdown('</div>', unsafe_allow_html=True)
