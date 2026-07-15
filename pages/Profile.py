import streamlit as st
from auth.session import require_auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from utils.helpers import inject_custom_css
from utils.validators import validate_email
from database.database import load_users, save_users
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SmartCampusAI - Profile",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Enforce authentication
require_auth()

# 2. Inject CSS styles
inject_custom_css()

# Render Navbar & Sidebar
render_navbar("User Profile")
render_sidebar("Profile")

user = st.session_state.user
user_id = user.get("id")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    # Profile Card Display
    with st.container(border=True):
        st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <div style="width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #a855f7); display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; color: white; font-weight: bold; font-size: 40px; box-shadow: 0 4px 15px rgba(99,102,241,0.3);">
                {user.get("name", "U")[0].upper()}
            </div>
            <h2 style="margin: 0; color: #f3f4f6;">{user.get("name", "Student")}</h2>
            <p style="margin: 5px 0 20px 0; color: #9ca3af; font-size: 14px;">@{user.get("username", "username")}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Details list
        created_str = "N/A"
        if user.get("created_at"):
            try:
                dt = datetime.fromisoformat(user["created_at"])
                created_str = dt.strftime("%B %d, %Y at %H:%M")
            except Exception:
                created_str = str(user["created_at"])
                
        last_login_str = "N/A"
        if user.get("last_login"):
            try:
                dt = datetime.fromisoformat(user["last_login"])
                last_login_str = dt.strftime("%B %d, %Y at %H:%M")
            except Exception:
                last_login_str = str(user["last_login"])
                
        st.markdown(f"""
        <div style="font-size: 14px; padding: 5px 10px; line-height: 2;">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 8px 0;">
                <span style="color: #9ca3af;">Account ID</span>
                <strong style="color: #f3f4f6;">#{user_id}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 8px 0;">
                <span style="color: #9ca3af;">Registered Email</span>
                <strong style="color: #f3f4f6;">{user.get("email", "N/A")}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.04); padding: 8px 0;">
                <span style="color: #9ca3af;">Created At</span>
                <strong style="color: #f3f4f6;">{created_str}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 8px 0;">
                <span style="color: #9ca3af;">Last Login</span>
                <strong style="color: #f3f4f6;">{last_login_str}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    # Update profile Form
    with st.container(border=True):
        st.markdown("<h3 style='margin-top: 0; color: #f3f4f6;'>✏️ Update Profile Details</h3>", unsafe_allow_html=True)
        st.write("You can update your display name and email address. Modifying your username is disabled for integrity.")
        
        new_name = st.text_input("Full Name", value=user.get("name", ""))
        new_email = st.text_input("Email Address", value=user.get("email", ""))
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        if st.button("Save Changes", key="profile_update_btn"):
            new_name = new_name.strip()
            new_email = new_email.strip()
            
            # Validation
            if not new_name or not new_email:
                st.error("Fields cannot be empty.")
            elif not validate_email(new_email):
                st.error("Invalid email address formatting.")
            else:
                # Load database and check duplicate email
                data = load_users()
                users = data.get("users", [])
                
                # Verify email duplicate (excluding current user)
                email_duplicate = False
                for u in users:
                    if u["id"] != user_id and u["email"].lower() == new_email.lower():
                        email_duplicate = True
                        break
                        
                if email_duplicate:
                    st.error("This email is already registered to another user.")
                else:
                    # Perform update
                    for u in users:
                        if u["id"] == user_id:
                            u["name"] = new_name
                            u["email"] = new_email
                            break
                            
                    data["users"] = users
                    save_users(data)
                    
                    # Update local session
                    user["name"] = new_name
                    user["email"] = new_email
                    st.session_state.user = user
                    
                    st.success("Profile updated successfully!")
                    st.rerun()
