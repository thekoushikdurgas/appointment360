"""
Dashboard Page - Overview statistics
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import text
from config.database import get_db
from services.contact_service import ContactService
from components.sidebar import show_sidebar
from utils.custom_styles import apply_global_styles
from components.ui_components import hero_section
from utils.theme_manager import ThemeManager

# Page config
st.set_page_config(
    page_title="Dashboard - Contact Management System",
    page_icon="🏠",
    layout="wide"
)

# Apply global styles
apply_global_styles()

show_sidebar()

# Hero Section
hero_section("🏠 Dashboard", "Welcome to your contact management hub")

st.markdown("---")

# Initialize database session
db = next(get_db())
contact_service = ContactService(db)

# Get statistics
stats = contact_service.get_contact_stats()

# Key Metrics with Icons
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
                padding: 1.5rem;
                border-radius: 12px;
                color: white;
                text-align: center;
                box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);">
        <h1 style="margin: 0; color: white;">📇</h1>
        <h2 style="margin: 0.5rem 0; color: white;">{}</h2>
        <p style="margin: 0; opacity: 0.9;">Total Contacts</p>
    </div>
    """.format(stats['total']), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
                padding: 1.5rem;
                border-radius: 12px;
                color: white;
                text-align: center;
                box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);">
        <h1 style="margin: 0; color: white;">🏭</h1>
        <h2 style="margin: 0.5rem 0; color: white;">{}</h2>
        <p style="margin: 0; opacity: 0.9;">Industries</p>
    </div>
    """.format(stats['industries']), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2196F3 0%, #64B5F6 100%);
                padding: 1.5rem;
                border-radius: 12px;
                color: white;
                text-align: center;
                box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);">
        <h1 style="margin: 0; color: white;">🌍</h1>
        <h2 style="margin: 0.5rem 0; color: white;">{}</h2>
        <p style="margin: 0; opacity: 0.9;">Countries</p>
    </div>
    """.format(stats['countries']), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%);
                padding: 1.5rem;
                border-radius: 12px;
                color: white;
                text-align: center;
                box-shadow: 0 4px 12px rgba(156, 39, 176, 0.3);">
        <h1 style="margin: 0; color: white;">✅</h1>
        <h2 style="margin: 0.5rem 0; color: white;">{}</h2>
        <p style="margin: 0; opacity: 0.9;">Active Contacts</p>
    </div>
    """.format(stats['active']), unsafe_allow_html=True)

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Industry Distribution")
    industries_result = db.execute(text("SELECT industry, COUNT(*) as count FROM contacts GROUP BY industry ORDER BY count DESC LIMIT 10"))
    industries_data = industries_result.fetchall()
    if industries_data:
        industries = [row[0] for row in industries_data]
        counts = [row[1] for row in industries_data]
        
        # Apply theme-aware colors
        theme = ThemeManager.get_theme()
        color_map = ['#FF6B35', '#4CAF50', '#2196F3', '#9C27B0', '#FF9800', '#F44336', '#00BCD4', '#8BC34A', '#E91E63', '#607D8B']
        
        # Create figure without color scale if only one value
        if len(set(counts)) <= 1:
            fig = px.bar(x=counts, y=industries, orientation='h', 
                         labels={'x': 'Count', 'y': 'Industry'})
        else:
            fig = px.bar(x=counts, y=industries, orientation='h', 
                         labels={'x': 'Count', 'y': 'Industry'},
                         color=counts, color_continuous_scale=color_map)
        fig.update_traces(marker_color=color_map[0] if color_map else '#FF6B35')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            font_size=11
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No industry data available")

with col2:
    st.markdown("### 🌍 Country Distribution")
    countries_result = db.execute(text("SELECT country, COUNT(*) as count FROM contacts GROUP BY country ORDER BY count DESC LIMIT 10"))
    countries_data = countries_result.fetchall()
    if countries_data:
        countries = [row[0] for row in countries_data]
        counts = [row[1] for row in countries_data]
        
        # Create figure without color scale if only one value
        if len(set(counts)) <= 1:
            fig = px.bar(x=counts, y=countries, orientation='h',
                         labels={'x': 'Count', 'y': 'Country'})
        else:
            fig = px.bar(x=counts, y=countries, orientation='h',
                         labels={'x': 'Count', 'y': 'Country'},
                         color=counts, color_continuous_scale=['#4CAF50'])
        fig.update_traces(marker_color='#4CAF50')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            font_size=11
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No country data available")

st.markdown("---")

# Quick Actions
st.markdown("### 🚀 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📇 View All Contacts", use_container_width=True, 
                help="Browse and manage all your contacts"):
        st.switch_page("pages/2_📇_Contacts.py")

with col2:
    if st.button("📤 Import Contacts", use_container_width=True,
                help="Import contacts from CSV files"):
        st.switch_page("pages/3_📤_Import_Contacts.py")

with col3:
    if st.button("📊 View Analytics", use_container_width=True,
                help="View detailed analytics and insights"):
        st.switch_page("pages/6_📊_Analytics.py")
