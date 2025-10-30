"""
Contact Management System - Main Application
Entry point for the Streamlit application
"""
import streamlit as st
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.auth_service_supabase import check_authentication, show_login, show_signup
from config.settings import PAGE_TITLE, PAGE_ICON
from utils.custom_styles import apply_global_styles

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main entry point"""
    # Apply global styles
    apply_global_styles()
    
    # Check authentication
    if not check_authentication():
        # Show sign up form if requested
        if st.session_state.get('show_signup', False):
            show_signup()
        else:
            show_login()
    else:
        # Show sidebar and redirect to dashboard
        from components.sidebar import show_sidebar
        show_sidebar()
        st.switch_page("pages/1_🏠_Dashboard.py")


if __name__ == "__main__":
    main()

