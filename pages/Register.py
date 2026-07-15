import streamlit as st
from auth.session import require_guest
from auth.authentication import register_user
from utils.helpers import inject_custom_css, load_lottie_url
from streamlit_lottie import st_lottie
import os

# Page configuration
st.set_page_config(
    page_title="SmartCampusAI - Register",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. Enforce guest status (redirects logged in users to Dashboard)
require_guest()

# 2. Inject custom CSS and background image styling
inject_custom_css()

# Hide default sidebar toggle for the registration screen
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
        Join the Future
    </h1>
    <h3 style='color: #e5e7eb; font-weight: 500; font-size: 22px; margin-top: 0;'>
        Create your SmartCampusAI account.
    </h3>
    <p style='color: #9ca3af; font-size: 15px; line-height: 1.6; max-width: 500px;'>
        Create an account to access customized insights, collaborate with our integrated AI assistant, and keep track of your performance logs.
    </p>
    """, unsafe_allow_html=True)
    
    # Load Lottie Animation
    lottie_url = "https://lottie.host/790105cc-7d0c-4ec1-912b-312ecf0426bb/J0T2y1Pq6y.json" # Tech network
    lottie_json = load_lottie_url(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, height=350, key="register_anim")
    else:
        st.markdown("<div style='height: 350px;'></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # Register form inside a glassmorphic container
    with st.container(border=True):
        st.markdown("""
        <h2 style='text-align: center; color: #f3f4f6; font-weight: 700; margin-top: 0; margin-bottom: 25px;'>
            Create Account
        </h2>
        """, unsafe_allow_html=True)
        
        name = st.text_input("Full Name", placeholder="e.g. John Doe", key="reg_name")
        username = st.text_input("Username", placeholder="e.g. johndoe", key="reg_username")
        email = st.text_input("Email Address", placeholder="e.g. john@example.com", key="reg_email")
        password = st.text_input("Password", type="password", placeholder="At least 8 characters", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="reg_confirm_password")
        
        # Display password requirements hint helper
        st.markdown("""
        <div style='font-size: 11px; color: #9ca3af; line-height: 1.4; margin: 5px 0 15px 0;'>
            🔑 Password must have: 8+ characters, 1 uppercase letter, 1 lowercase letter, 1 number.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Register & Get Started", key="register_submit_btn"):
            result = register_user(name, username, email, password, confirm_password)
            if result["success"]:
                st.success("Account successfully created! Redirecting to login...")
                # Add delay or just redirect
                st.info("Please log in with your credentials.")
                st.switch_page("pages/Login.py")
            else:
                st.error(result["message"])
                
        st.markdown("""
        <hr style='border-color: rgba(255, 255, 255, 0.08); margin: 20px 0 12px 0;' />
        <div style='text-align: center; color: #9ca3af; font-size: 13px; margin-bottom: 12px;'>
            Already have an account?
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("Back to Login", key="register_login_nav"):
            st.switch_page("pages/Login.py")
        st.markdown('</div>', unsafe_allow_html=True)
