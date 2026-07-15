import streamlit as st
from auth.session import require_auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from utils.helpers import inject_custom_css
from utils.config import APP_NAME, MODEL_NAME, SESSION_TIMEOUT_SEC, API_KEY
from utils.validators import validate_password
from database.database import load_users, save_users
from auth.password_utils import verify_password, hash_password

# Page configuration
st.set_page_config(
    page_title="SmartCampusAI - Settings",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Enforce authentication
require_auth()

# 2. Inject CSS styles
inject_custom_css()

# Render Navbar & Sidebar
render_navbar("App Settings")
render_sidebar("Settings")

user = st.session_state.user
user_id = user.get("id")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.1, 1], gap="large")

with col_left:
    # App Settings & Environment Variables Status
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0; color: #f3f4f6;'>⚙️ Application Configuration</h3>", unsafe_allow_html=True)
        st.write("Below are the configuration variables loaded from the `.env` file.")
        
        # Display table or metadata cards
        api_key_status = "✅ CONFIGURED (Hidden)" if API_KEY else "❌ NOT SET"
        
        st.markdown(f"""
        <div style="font-size: 14px; padding: 5px 10px; line-height: 2.2;">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 8px 0;">
                <span style="color: #9ca3af;">Application Name</span>
                <strong style="color: #f3f4f6;">{APP_NAME}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 8px 0;">
                <span style="color: #9ca3af;">LLM Model Version</span>
                <strong style="color: #a855f7;">{MODEL_NAME}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 8px 0;">
                <span style="color: #9ca3af;">Session Inactivity Timeout</span>
                <strong style="color: #f3f4f6;">{SESSION_TIMEOUT_SEC // 60} minutes ({SESSION_TIMEOUT_SEC}s)</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 8px 0;">
                <span style="color: #9ca3af;">Campus API Key</span>
                <strong style="color: #10b981;">{api_key_status}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # UI Customization mock
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0; color: #f3f4f6;'>🎨 Interface Customization</h3>", unsafe_allow_html=True)
        st.write("Adjust client-side interface configurations.")
        
        theme_opt = st.selectbox("Dashboard Theme", ["Glassmorphism Indigo (Default)", "Cyberpunk Neon", "Midnight Dark", "Stellar Blue"], disabled=True)
        st.markdown("<div style='font-size: 11px; color: #9ca3af; margin-top: -5px;'>Note: Themes are locked to environment styling options.</div>", unsafe_allow_html=True)
        
        density = st.radio("Interface Density", ["Comfortable", "Compact"], index=0, horizontal=True)

with col_right:
    # Security / Change Password Form
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0; color: #f3f4f6;'>🔒 Security & Password</h3>", unsafe_allow_html=True)
        st.write("Change your account password securely.")
        
        old_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_new = st.text_input("Confirm New Password", type="password")
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        if st.button("Update Password", key="password_update_btn"):
            if not old_password or not new_password or not confirm_new:
                st.error("All fields are required to update password.")
            elif new_password != confirm_new:
                st.error("New passwords do not match.")
            else:
                # Validate strength
                pwd_chk = validate_password(new_password)
                if not pwd_chk["valid"]:
                    st.error(pwd_chk["message"])
                else:
                    # Load users database
                    data = load_users()
                    users = data.get("users", [])
                    
                    # Verify current password and update
                    pwd_updated = False
                    error_msg = ""
                    for u in users:
                        if u["id"] == user_id:
                            # Verify if old password is correct
                            if verify_password(old_password, u["password"]):
                                u["password"] = hash_password(new_password)
                                pwd_updated = True
                            else:
                                error_msg = "Incorrect current password."
                            break
                            
                    if pwd_updated:
                        save_users(data)
                        st.success("Password updated successfully!")
                    else:
                        st.error(error_msg if error_msg else "User not found in database.")
                        
        st.markdown("""
        <div style='font-size: 11px; color: #9ca3af; line-height: 1.4; margin-top: 15px;'>
            💡 Tip: SmartCampusAI passwords require: 8+ characters, 1 uppercase, 1 lowercase, 1 number.
        </div>
        """, unsafe_allow_html=True)
