"""
Theme Manager - Dark/Light Theme System
"""
import streamlit as st


class ThemeManager:
    """Manage theme state and CSS injection"""
    
    # Light Theme Colors
    LIGHT_THEME = {
        'backgroundColor': '#FFFFFF',
        'primaryColor': '#FF6B35',
        'secondaryBackgroundColor': '#F5F5F5',
        'textColor': '#1A1A1A',
        'borderColor': '#E0E0E0',
        'successColor': '#4CAF50',
        'errorColor': '#F44336',
        'warningColor': '#FF9800',
        'infoColor': '#2196F3',
    }
    
    # Dark Theme Colors (Warm tones with brown/orange)
    DARK_THEME = {
        'backgroundColor': '#1A1410',
        'primaryColor': '#FF8C42',
        'secondaryBackgroundColor': '#2D2416',
        'textColor': '#E8D5C4',
        'borderColor': '#3D3328',
        'successColor': '#81C784',
        'errorColor': '#E57373',
        'warningColor': '#FFB74D',
        'infoColor': '#64B5F6',
    }
    
    @staticmethod
    def get_theme():
        """Get current theme preference"""
        if 'theme' not in st.session_state:
            st.session_state.theme = 'light'
        return st.session_state.theme
    
    @staticmethod
    def set_theme(theme: str):
        """Set theme preference (light or dark)"""
        if theme in ['light', 'dark']:
            st.session_state.theme = theme
        else:
            raise ValueError("Theme must be 'light' or 'dark'")
    
    @staticmethod
    def toggle_theme():
        """Toggle between light and dark themes"""
        current = ThemeManager.get_theme()
        new_theme = 'dark' if current == 'light' else 'light'
        ThemeManager.set_theme(new_theme)
        return new_theme
    
    @staticmethod
    def get_colors():
        """Get color palette for current theme"""
        theme = ThemeManager.get_theme()
        return ThemeManager.DARK_THEME if theme == 'dark' else ThemeManager.LIGHT_THEME
    
    @staticmethod
    def inject_custom_css():
        """Inject custom CSS for theme styling"""
        colors = ThemeManager.get_colors()
        
        css = f"""
        <style>
        /* Root Variables */
        :root {{
            --bg-color: {colors['backgroundColor']};
            --secondary-bg: {colors['secondaryBackgroundColor']};
            --text-color: {colors['textColor']};
            --primary-color: {colors['primaryColor']};
            --border-color: {colors['borderColor']};
        }}
        
        /* Main Container */
        .main {{
            background-color: var(--bg-color) !important;
        }}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--secondary-bg);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--primary-color);
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {colors['primaryColor']}DD;
        }}
        
        /* Enhanced Buttons */
        .stButton > button {{
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            font-weight: 500 !important;
            border: 1px solid var(--border-color) !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
        }}
        
        /* Primary Button */
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {colors['primaryColor']}, {colors['primaryColor']}DD);
            border: none !important;
        }}
        
        /* Secondary Button */
        .stButton > button[kind="secondary"] {{
            background: var(--secondary-bg);
            color: var(--text-color);
        }}
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {{
            border-radius: 8px !important;
            border: 1px solid var(--border-color) !important;
            background-color: var(--bg-color) !important;
            color: var(--text-color) !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 3px {colors['primaryColor']}22 !important;
        }}
        
        /* Metrics */
        [data-testid="stMetricValue"] {{
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: var(--primary-color) !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: var(--text-color) !important;
            font-weight: 500 !important;
        }}
        
        /* Sidebar */
        .css-1d391kg {{
            background-color: var(--secondary-bg) !important;
        }}
        
        /* Cards */
        .element-container {{
            border-radius: 12px;
            padding: 1rem;
            background-color: var(--secondary-bg);
            border: 1px solid var(--border-color);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }}
        
        .element-container:hover {{
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
        }}
        
        /* Tables */
        .stDataFrame {{
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: var(--secondary-bg);
            border-radius: 8px;
            padding: 4px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            border-radius: 6px;
            padding: 8px 16px;
            transition: all 0.2s ease;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: var(--primary-color);
            color: white !important;
        }}
        
        /* Success/Error Messages */
        .stAlert > div > div > div > div {{
            border-radius: 8px;
            border-left: 4px solid;
        }}
        
        /* Checkboxes and Radio */
        .stCheckbox label,
        .stRadio label {{
            color: var(--text-color) !important;
        }}
        
        /* Progress Bars */
        .stProgress > div > div > div > div {{
            background-color: var(--primary-color) !important;
        }}
        
        /* Search Input Enhancement */
        input[placeholder*="Search"] {{
            border-radius: 20px !important;
            padding-left: 2.5rem !important;
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)
    
    @staticmethod
    def get_plotly_template():
        """Get Plotly template for current theme"""
        theme = ThemeManager.get_theme()
        
        if theme == 'dark':
            return {
                'layout': {
                    'plot_bgcolor': '#2D2416',
                    'paper_bgcolor': '#1A1410',
                    'font': {'color': '#E8D5C4'},
                    'colorway': ['#FF8C42', '#FF6B35', '#FFA07A', '#FF8C6B', '#FF7F50', '#FF6347', '#FF5722', '#FF4500']
                }
            }
        else:
            return {
                'layout': {
                    'plot_bgcolor': 'white',
                    'paper_bgcolor': 'white',
                    'font': {'color': '#1A1A1A'},
                    'colorway': ['#FF6B35', '#FF8C42', '#FFA07A', '#4CAF50', '#2196F3', '#9C27B0', '#F44336', '#FF9800']
                }
            }
