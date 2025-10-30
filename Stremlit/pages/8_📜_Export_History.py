"""
Export History Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from config.database import get_db
from components.sidebar import show_sidebar
from utils.custom_styles import apply_global_styles
from components.ui_components import hero_section

st.set_page_config(
    page_title="Export History - Contact Management System",
    page_icon="📜",
    layout="wide"
)

# Apply global styles
apply_global_styles()

show_sidebar()

# Hero Section
hero_section("📜 Export History", "View your data export history and download records")

st.markdown("---")

db = next(get_db())

# Mock export history data
st.info("👷 Export history tracking coming soon!")

# Example display
if st.button("Show Mock History"):
    sample_data = [
        {
            'Date': '2024-01-15',
            'Type': 'All Contacts',
            'Format': 'Excel',
            'Records': 1250,
            'Filename': 'export_all_20240115.xlsx'
        },
        {
            'Date': '2024-01-14',
            'Type': 'Filtered',
            'Format': 'CSV',
            'Records': 85,
            'Filename': 'export_filtered_20240114.csv'
        },
        {
            'Date': '2024-01-13',
            'Type': 'Selected',
            'Format': 'Excel',
            'Records': 42,
            'Filename': 'export_selected_20240113.xlsx'
        }
    ]
    
    df = pd.DataFrame(sample_data)
    st.dataframe(df, width='stretch')
