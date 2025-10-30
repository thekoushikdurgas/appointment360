"""
Settings Page
"""
import streamlit as st
from components.sidebar import show_sidebar
from utils.custom_styles import apply_global_styles
from components.ui_components import hero_section
from utils.theme_manager import ThemeManager

st.set_page_config(
    page_title="Settings - Contact Management System",
    page_icon="⚙️",
    layout="wide"
)

# Apply global styles
apply_global_styles()

show_sidebar()

# Hero Section
hero_section("⚙️ Settings", "Manage your account preferences and settings")

st.markdown("---")

# Settings tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎨 Appearance", "👤 Profile", "🔒 Security", "🌍 Preferences"])

with tab1:
    st.markdown("### 🎨 Theme & Appearance Settings")
    
    current_theme = ThemeManager.get_theme()
    st.info(f"Current theme: **{current_theme.title()}**")
    
    # Theme preview cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            border: 2px solid #FF6B35;
            border-radius: 12px;
            padding: 2rem;
            background: linear-gradient(135deg, #FFFFFF 0%, #F5F5F5 100%);
            text-align: center;
        ">
            <h2 style="color: #FF6B35;">☀️ Light Theme</h2>
            <p style="color: #666;">Clean, bright interface</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Switch to Light Theme", use_container_width=True,
                    type="primary" if current_theme == 'light' else "secondary",
                    key="theme_light_preview"):
            ThemeManager.set_theme('light')
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="
            border: 2px solid #FF8C42;
            border-radius: 12px;
            padding: 2rem;
            background: linear-gradient(135deg, #1A1410 0%, #2D2416 100%);
            text-align: center;
            color: #E8D5C4;
        ">
            <h2 style="color: #FF8C42;">🌙 Dark Theme</h2>
            <p style="color: #E8D5C4;">Warm, eye-friendly interface</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Switch to Dark Theme", use_container_width=True,
                    type="primary" if current_theme == 'dark' else "secondary",
                    key="theme_dark_preview"):
            ThemeManager.set_theme('dark')
            st.rerun()
    
    st.markdown("---")
    st.markdown("**Note:** Theme changes are applied immediately and persist across sessions.")

with tab2:
    st.markdown("### 👤 Profile Settings")
    
    if 'user' in st.session_state and st.session_state.user:
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("👤 First Name", placeholder="Your first name")
                email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            
            with col2:
                last_name = st.text_input("👤 Last Name", placeholder="Your last name")
                role = st.text_input("👔 Role", placeholder="Your role/position", disabled=True)
            
            if st.form_submit_button("💾 Save Profile", type="primary", use_container_width=True):
                st.success("✅ Profile updated successfully!")
    else:
        st.info("Please log in to view your profile settings")

with tab3:
    st.markdown("### 🔒 Security Settings")
    
    with st.form("password_form"):
        current_password = st.text_input("🔒 Current Password", type="password",
                                         help="Enter your current password")
        new_password = st.text_input("🔒 New Password", type="password",
                                     help="Choose a strong password (min 8 characters)")
        confirm_password = st.text_input("🔒 Confirm New Password", type="password",
                                         help="Re-enter your new password")
        
        if st.form_submit_button("🔐 Update Password", type="primary", use_container_width=True):
            if new_password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(new_password) < 8:
                st.error("❌ Password must be at least 8 characters long")
            else:
                st.success("✅ Password updated successfully!")

with tab4:
    st.markdown("### 🌍 Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox("🗣️ Language", ["English", "Spanish", "French", "German"])
        date_format = st.selectbox("📅 Date Format", ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"])
    
    with col2:
        timezone = st.selectbox("🕐 Timezone", ["UTC", "EST", "PST", "GMT", "CET"])
        notif_emails = st.checkbox("📧 Email Notifications", value=True)
    
    if st.button("💾 Save Preferences", type="primary", use_container_width=True):
        st.success("✅ Preferences saved successfully!")
