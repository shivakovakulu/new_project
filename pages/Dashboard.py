import streamlit as st
from auth.session import require_auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from components.cards import render_kpi_cards
from utils.helpers import inject_custom_css, load_lottie_url
from utils.config import MODEL_NAME
from streamlit_lottie import st_lottie
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SmartCampusAI - Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Enforce authentication status (redirects guest users to Login)
require_auth()

# 2. Inject custom CSS and background image styling
inject_custom_css()

# Get the current user details from session state
user = st.session_state.user
name = user.get("name", "Student")
username = user.get("username", "user")
email = user.get("email", "john@example.com")
created_at = user.get("created_at", datetime.now().isoformat())
last_login = user.get("last_login")

# 3. Render Custom Top Navbar
render_navbar("Dashboard")

# 4. Render Custom Sidebar
render_sidebar("Dashboard")

# 5. Render Analytical Metrics Cards
render_kpi_cards(last_login)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# 6. Main Dashboard Layout Section
col_left, col_right = st.columns([1.5, 1], gap="medium")

with col_left:
    # Welcome banner card
    with st.container(border=True):
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1 style='margin: 0 0 10px 0; color: #f3f4f6; font-size: 28px; font-weight: 700;'>
                    Welcome back, {name}! 👋
                </h1>
                <p style='color: #9ca3af; font-size: 14px; margin: 0; line-height: 1.5;'>
                    Here is what's happening at SmartCampus today. You can monitor user database registries, chat with the AI assistant, or customize your configurations in Settings.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # AI Assistant panel
    with st.container(border=True):
        st.markdown(f"""
        <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;'>
            <h3 style='margin: 0; color: #f3f4f6;'>🤖 Interactive AI Assistant</h3>
            <span class="status-badge status-active" style="font-size: 11px;">Powered by {MODEL_NAME}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple AI Chat simulation
        st.write("Ask the campus assistant anything about schedule, courses, directory, or campus events:")
        
        user_query = st.text_input("Ask AI...", placeholder="e.g. Find all engineering buildings, or list library hours", label_visibility="collapsed")
        
        if user_query:
            with st.spinner("AI thinking..."):
                import time
                time.sleep(0.8) # Simulate AI response delay
                
                # Dynamic Mock Responses based on keywords
                query_lower = user_query.lower()
                if "library" in query_lower:
                    response = "📚 **Campus Library Hours:** Today the library is open from 8:00 AM to 10:00 PM. The study rooms can be reserved on the second floor."
                elif "building" in query_lower or "map" in query_lower:
                    response = "🏢 **Campus Buildings:** The engineering complex is located in Section B, while the Science and Arts lecture halls are in Section A & C respectively."
                elif "class" in query_lower or "schedule" in query_lower:
                    response = "🗓️ **Your Schedule:** You have 'Introduction to Machine Learning' scheduled today at 2:00 PM in Room 402."
                else:
                    response = f"🤖 **SmartCampusAI Response:** Thank you for asking. Regarding '{user_query}', all systems are fully functional, and your campus records indicate that academic queries can be configured via Settings."
                
                st.markdown(f"""
                <div style="background: rgba(99, 102, 241, 0.08); border-left: 4px solid #6366f1; padding: 15px; border-radius: 4px 10px 10px 4px; margin-top: 15px; color: #e5e7eb;">
                    {response}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💡 Tip: Try asking about 'library hours' or 'class schedule' to see response triggers.")

with col_right:
    # Notifications Card
    with st.container(border=True):
        st.markdown("<h3 style='margin: 0 0 15px 0; color: #f3f4f6;'>🔔 Campus Notifications</h3>", unsafe_allow_html=True)
        
        notifications = [
            {"time": "10 Mins Ago", "title": "Database back-up successful", "desc": "Local database users.json backup written to disk.", "icon": "💾"},
            {"time": "1 Hour Ago", "title": "New registration logged", "desc": "A new administrator account was registered.", "icon": "👤"},
            {"time": "Yesterday", "title": "System maintenance scheduled", "desc": "Campus server maintenance at Sunday 03:00 AM.", "icon": "⚙️"}
        ]
        
        for item in notifications:
            st.markdown(f"""
            <div style="display: flex; gap: 12px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <div style="font-size: 20px;">{item['icon']}</div>
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <span style="font-weight: 600; font-size: 14px; color: #f3f4f6;">{item['title']}</span>
                        <span style="font-size: 11px; color: #9ca3af;">{item['time']}</span>
                    </div>
                    <div style="font-size: 12px; color: #9ca3af; margin-top: 2px;">{item['desc']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Recent Activity logs
    with st.container(border=True):
        st.markdown("<h3 style='margin: 0 0 15px 0; color: #f3f4f6;'>⏱️ Recent Activity</h3>", unsafe_allow_html=True)
        
        activities = [
            {"event": "User Login", "detail": f"Account @{username} authenticated successfully.", "time": "Just now"},
            {"event": "Session Started", "detail": "Session token generated with 30m idle timeout.", "time": "1 min ago"},
            {"event": "Environment Initialized", "detail": "Dotenv configuration loaded system variables.", "time": "5 mins ago"}
        ]
        
        for act in activities:
            st.markdown(f"""
            <div style="margin-bottom: 12px; font-size: 13px;">
                <div style="display: flex; justify-content: space-between;">
                    <strong style="color: #6366f1;">{act['event']}</strong>
                    <span style="color: #9ca3af; font-size: 11px;">{act['time']}</span>
                </div>
                <div style="color: #d1d5db; font-size: 12px; margin-top: 2px;">{act['detail']}</div>
            </div>
            """, unsafe_allow_html=True)
