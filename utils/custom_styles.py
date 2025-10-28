"""
Custom Global Styles for the Application
"""
import streamlit as st
from utils.theme_manager import ThemeManager


def apply_global_styles():
    """Apply global custom styles to the app"""
    ThemeManager.inject_custom_css()
    
    colors = ThemeManager.get_colors()
    
    additional_css = f"""
    <style>
    /* Additional Global Styles */
    
    /* Page Title Styling */
    h1 {{
        color: {colors['primaryColor']} !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }}
    
    /* Subtitle/Separator */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            {colors['primaryColor']}, 
            transparent);
        margin: 2rem 0;
    }}
    
    /* Links */
    a {{
        color: {colors['primaryColor']} !important;
        text-decoration: none;
        transition: all 0.2s ease;
    }}
    
    a:hover {{
        text-decoration: underline;
    }}
    
    /* Code Blocks */
    pre, code {{
        background-color: {colors['secondaryBackgroundColor']} !important;
        border: 1px solid {colors['borderColor']};
        border-radius: 6px;
        padding: 0.5rem;
    }}
    
    /* Markdown Tables */
    table {{
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
        width: 100%;
        border: 1px solid {colors['borderColor']};
    }}
    
    th {{
        background-color: {colors['secondaryBackgroundColor']} !important;
        color: {colors['primaryColor']} !important;
        font-weight: 600 !important;
        padding: 0.75rem !important;
    }}
    
    td {{
        padding: 0.75rem !important;
        border-bottom: 1px solid {colors['borderColor']};
    }}
    
    tr:hover {{
        background-color: {colors['secondaryBackgroundColor']} !important;
    }}
    
    /* Selectbox Enhancement */
    .stSelectbox > div > div > div {{
        background-color: {colors['backgroundColor']} !important;
    }}
    
    /* Multiselect */
    .stMultiSelect > div > div {{
        border-radius: 8px !important;
        border: 1px solid {colors['borderColor']} !important;
    }}
    
    /* File Uploader */
    .stFileUploader > div > div {{
        border-radius: 12px !important;
        border: 2px dashed {colors['borderColor']} !important;
        background-color: {colors['secondaryBackgroundColor']} !important;
        transition: all 0.3s ease;
    }}
    
    .stFileUploader > div > div:hover {{
        border-color: {colors['primaryColor']} !important;
        background-color: {colors['primaryColor']}11 !important;
    }}
    
    /* Spinner */
    .stSpinner > div {{
        border-top-color: {colors['primaryColor']} !important;
    }}
    
    /* Success/Error/Warning/Info Colors */
    .alert-success {{
        background-color: {colors['successColor']}22 !important;
        border-left: 4px solid {colors['successColor']} !important;
        color: {colors['successColor']} !important;
    }}
    
    .alert-error {{
        background-color: {colors['errorColor']}22 !important;
        border-left: 4px solid {colors['errorColor']} !important;
        color: {colors['errorColor']} !important;
    }}
    
    .alert-warning {{
        background-color: {colors['warningColor']}22 !important;
        border-left: 4px solid {colors['warningColor']} !important;
        color: {colors['warningColor']} !important;
    }}
    
    .alert-info {{
        background-color: {colors['infoColor']}22 !important;
        border-left: 4px solid {colors['infoColor']} !important;
        color: {colors['infoColor']} !important;
    }}
    </style>
    """
    
    st.markdown(additional_css, unsafe_allow_html=True)


def get_status_badge_html(text: str, status: str = "info"):
    """Generate HTML for a status badge"""
    colors = {
        'success': ('#4CAF50', '✅'),
        'error': ('#F44336', '❌'),
        'warning': ('#FF9800', '⚠️'),
        'info': ('#2196F3', 'ℹ️'),
        'pending': ('#FF9800', '⏳'),
        'completed': ('#4CAF50', '✅')
    }
    
    color, icon = colors.get(status, colors['info'])
    
    return f"""
    <span style="
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background-color: {color}22;
        color: {color};
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 500;
        border: 1px solid {color}44;
    ">
        {icon} {text}
    </span>
    """

