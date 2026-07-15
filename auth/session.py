import time
import streamlit as st
from utils.config import SESSION_TIMEOUT_SEC

def init_session() -> None:
    """Initialize necessary session state variables for authentication and activity tracking."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = time.time()

def check_session_timeout() -> None:
    """Check if the user session has timed out due to inactivity. Logs out if timeout is reached."""
    init_session()
    
    if st.session_state.authenticated:
        current_time = time.time()
        elapsed_time = current_time - st.session_state.last_activity
        
        if elapsed_time > SESSION_TIMEOUT_SEC:
            logout()
            st.warning("Your session has expired due to inactivity. Please log in again.")
            st.stop()
        else:
            # Update last activity timestamp
            st.session_state.last_activity = current_time

def login(user_data: dict) -> None:
    """Log in the user, set session variables, and update activity log."""
    st.session_state.authenticated = True
    st.session_state.user = user_data
    st.session_state.last_activity = time.time()

def logout() -> None:
    """Clear session authentication state and redirect to login."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.last_activity = time.time()
    
    # Trigger a rerun to ensure UI updates and redirects take effect
    st.rerun()

def require_auth() -> None:
    """
    Protect a page. If user is not authenticated, redirects to the Login page.
    Should be called at the very top of protected pages (Dashboard, Profile, Settings).
    """
    init_session()
    check_session_timeout()
    
    if not st.session_state.authenticated:
        # Redirect to login page
        st.switch_page("pages/Login.py")
        st.stop()

def require_guest() -> None:
    """
    Redirect authenticated users to the Dashboard.
    Should be called at the top of guest-only pages (Login, Register).
    """
    init_session()
    
    if st.session_state.authenticated:
        st.switch_page("pages/Dashboard.py")
        st.stop()
