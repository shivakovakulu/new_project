import streamlit as st
from database.database import load_users
from utils.config import MODEL_NAME
from datetime import datetime

def render_kpi_cards(last_login_iso: str = None) -> None:
    """
    Render four custom-designed glassmorphism metric cards:
    1. Total Campus Users
    2. Session Status
    3. Last Login Time
    4. AI Engine Status
    """
    # 1. Fetch user count
    try:
        users_data = load_users()
        total_users = len(users_data.get("users", []))
    except Exception:
        total_users = 1
        
    # 2. Format Last Login
    last_login_str = "New Session"
    if last_login_iso:
        try:
            dt = datetime.fromisoformat(last_login_iso)
            last_login_str = dt.strftime("%b %d, %H:%M")
        except Exception:
            last_login_str = str(last_login_iso)
            
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-container">
                <div>
                    <div class="metric-title">Total Users</div>
                    <div class="metric-value">{total_users}</div>
                </div>
                <span class="metric-icon">👥</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-container">
                <div>
                    <div class="metric-title">Session Status</div>
                    <div class="metric-value" style="color: #10b981; font-size: 20px; font-weight: 600; padding: 5px 0;">CONNECTED</div>
                </div>
                <span class="metric-icon">🔐</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-container">
                <div>
                    <div class="metric-title">Last Login</div>
                    <div class="metric-value" style="font-size: 18px; font-weight: 600; padding: 6px 0;">{last_login_str}</div>
                </div>
                <span class="metric-icon">⏱️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-container">
                <div>
                    <div class="metric-title">AI Engine</div>
                    <div class="metric-value" style="color: #a855f7; font-size: 18px; font-weight: 600; padding: 6px 0;">{MODEL_NAME}</div>
                </div>
                <span class="metric-icon">🤖</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
