import base64
import os
import requests
import streamlit as st
from typing import Dict, Any, Optional

def get_base64_image(image_path: str) -> str:
    """Convert a local image file to a base64 string for CSS embedding."""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
    return ""

def inject_custom_css() -> None:
    """Load style.css and inject it along with base64 background image styling into Streamlit."""
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    style_path = os.path.join(assets_dir, "style.css")
    bg_path = os.path.join(assets_dir, "background.png")
    
    # Base layout style
    css_content = ""
    if os.path.exists(style_path):
        try:
            with open(style_path, "r") as f:
                css_content = f.read()
        except Exception as e:
            print(f"Error reading style.css: {e}")
            
    # Base64 encoded background for perfect performance
    bg_style = ""
    if os.path.exists(bg_path):
        bg_base64 = get_base64_image(bg_path)
        if bg_base64:
            bg_style = f"""
            <style>
            .stApp {{
                background-image: linear-gradient(135deg, rgba(11, 15, 25, 0.92), rgba(17, 24, 39, 0.95)), url("data:image/png;base64,{bg_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """
            
    st.markdown(f"<style>{css_content}</style>" + bg_style, unsafe_allow_html=True)

def load_lottie_url(url: str) -> Optional[Dict[str, Any]]:
    """Safely retrieve Lottie animation data from a given URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"Lottie load error: {e}")
    return None
