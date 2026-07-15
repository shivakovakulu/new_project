import streamlit as st
from datetime import datetime

def render_navbar(page_title: str) -> None:
    """
    Render a premium glassmorphic top navigation bar indicating current section,
    current date, and overall system status.
    """
    current_date = datetime.now().strftime("%A, %b %d, %Y")
    
    st.markdown(f"""
    <div class="navbar-custom">
        <div class="navbar-brand">
            SmartCampusAI <span style="font-size: 16px; font-weight: 400; color: #6b7280; margin: 0 10px;">/</span> <span style="font-size: 15px; font-weight: 500; color: #f3f4f6; text-transform: uppercase; letter-spacing: 0.5px;">{page_title}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="font-size: 13px; color: #9ca3af; font-weight: 500;">📅 {current_date}</span>
            <span class="status-badge status-active" style="padding: 4px 8px; font-size: 10px;">● Campus AI Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
