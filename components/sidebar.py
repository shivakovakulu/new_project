import streamlit as st
from streamlit_option_menu import option_menu
from auth.session import logout

def render_sidebar(current_page: str) -> None:
    """
    Render a custom sidebar menu. Handled dynamically according to authentication state
    and handles switching between pages via st.switch_page.
    """
    # 1. App branding / logo in sidebar
    import os
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width="stretch")
    else:
        st.sidebar.markdown("<h2 style='text-align: center; color: #6366f1;'>SmartCampusAI</h2>", unsafe_allow_html=True)
        
    # 2. Render user card in sidebar if logged in
    if st.session_state.get("authenticated") and st.session_state.get("user"):
        user = st.session_state.user
        st.sidebar.markdown(f"""
        <div style="text-align: center; padding: 15px; margin: 15px 0; background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; backdrop-filter: blur(10px);">
            <div style="width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #a855f7); display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto; color: white; font-weight: bold; font-size: 20px;">
                {user.get("name", "U")[0].upper()}
            </div>
            <h4 style="margin: 0; color: #f3f4f6; font-size: 15px;">{user.get("name", "Student")}</h4>
            <p style="margin: 2px 0 0 0; color: #9ca3af; font-size: 12px;">@{user.get("username", "user")}</p>
        </div>
        """, unsafe_allow_html=True)

    # 3. Sidebar Navigation options
    options = ["Dashboard", "Profile", "Settings", "Logout"]
    icons = ["house-door-fill", "person-fill", "gear-fill", "box-arrow-right"]
    
    # Map index
    try:
        default_index = options.index(current_page)
    except ValueError:
        default_index = 0
        
    with st.sidebar:
        st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin-top: 0;' />", unsafe_allow_html=True)
        selected = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            menu_icon=None,
            default_index=default_index,
            styles={
                "container": {"background-color": "transparent", "padding": "0px"},
                "icon": {"color": "#a855f7", "font-size": "15px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "5px 0px",
                    "color": "#9ca3af",
                    "border-radius": "8px",
                    "font-weight": "500",
                    "--hover-color": "rgba(255, 255, 255, 0.03)"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.15))",
                    "color": "#f3f4f6",
                    "border": "1px solid rgba(99, 102, 241, 0.3)",
                    "font-weight": "600"
                }
            }
        )
        
    # Navigation logic
    if selected == "Logout":
        logout()
    elif selected != current_page:
        # Switch pages using the relative pages directory path
        if selected == "Dashboard":
            st.switch_page("pages/Dashboard.py")
        elif selected == "Profile":
            st.switch_page("pages/Profile.py")
        elif selected == "Settings":
            st.switch_page("pages/Settings.py")
