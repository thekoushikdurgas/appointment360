"""
Sidebar Component with Theme Toggle
"""
import streamlit as st
from services.auth_service_supabase import logout_user, check_authentication
from utils.theme_manager import ThemeManager

def show_sidebar():
    """Display sidebar with navigation and theme toggle"""
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"
    
    # Theme Toggle Section
    st.sidebar.markdown("### 🌓 Theme")
    col1, col2 = st.sidebar.columns(2)
    current_theme = ThemeManager.get_theme()
    
    with col1:
        if st.button("☀️ Light", key="theme_light", 
                    type="primary" if current_theme == 'light' else "secondary"):
            ThemeManager.set_theme('light')
            st.rerun()
    
    with col2:
        if st.button("🌙 Dark", key="theme_dark",
                    type="primary" if current_theme == 'dark' else "secondary"):
            ThemeManager.set_theme('dark')
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # App Title
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #FF6B35; margin: 0;">📇 Contact Manager</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # User info
    if check_authentication():
        if 'user' in st.session_state and st.session_state.user:
            user_email = st.session_state.user.email if hasattr(st.session_state.user, 'email') else "User"
            
            # Styled user info card
            st.sidebar.markdown(f"""
            <div style="
                background: #F5F5F5;
                border-radius: 8px;
                padding: 0.75rem;
                margin: 0.5rem 0;
                border-left: 3px solid #FF6B35;
            ">
                <strong>👤 User</strong><br>
                <span style="color: #666; font-size: 0.9rem;">{user_email}</span>
            </div>
            """, unsafe_allow_html=True)
            st.sidebar.markdown("---")
    
    # Navigation
    st.sidebar.markdown("### 📋 Navigation")
    
    pages = [
        ("🏠 Dashboard", "pages/1_🏠_Dashboard.py", "Home"),
        ("📇 Contacts", "pages/2_📇_Contacts.py", "Manage contacts"),
        ("📤 Import", "pages/3_📤_Import_Contacts.py", "Import contacts"),
        ("📊 Analytics", "pages/6_📊_Analytics.py", "View analytics"),
        ("🔍 Quality", "pages/7_🔍_Data_Quality.py", "Data quality"),
        ("📜 Export", "pages/8_📜_Export_History.py", "Export history"),
        ("👥 Users", "pages/4_👥_User_Management.py", "User management"),
        ("⚙️ Settings", "pages/5_⚙️_Settings.py", "App settings"),
    ]
    
    for page_name, page_path, desc in pages:
        if st.sidebar.button(page_name, key=f"nav_{page_name}", use_container_width=True):
            st.switch_page(page_path)
    
    st.sidebar.markdown("---")
    
    # Logout button
    if check_authentication():
        if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout_user()
            st.rerun()
    
    # Progress tracker (if exists)
    try:
        from .progress_tracker import show_progress_tracker
        st.sidebar.markdown("---")
        show_progress_tracker()
    except:
        pass
