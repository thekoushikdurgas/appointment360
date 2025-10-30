"""
Analytics Page
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


def safe_db_execute(db, query):
    """Safely execute a database query with automatic rollback on error"""
    try:
        return db.execute(query)
    except Exception as e:
        try:
            db.rollback()
        except:
            pass
        # Try again after rollback
        return db.execute(query)

st.set_page_config(
    page_title="Analytics - Contact Management System",
    page_icon="📊",
    layout="wide"
)

# Apply global styles
apply_global_styles()

show_sidebar()

# Hero Section
hero_section("📊 Analytics", "Insights and statistics about your contacts")

st.markdown("---")

# Initialize database
db = next(get_db())

# Rollback any failed transactions from previous pages
try:
    db.rollback()
except:
    pass  # Ignore rollback errors

contact_service = ContactService(db)

# Get statistics
stats = contact_service.get_contact_stats()

# Key Metrics
st.markdown("### 📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Contacts",
        value=stats['total'],
        delta=f"{stats['active']} active"
    )

with col2:
    st.metric(
        label="Industries",
        value=stats['industries']
    )

with col3:
    st.metric(
        label="Countries",
        value=stats['countries']
    )

with col4:
    st.metric(
        label="Active Contacts",
        value=stats['active']
    )

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Industry Distribution")
    # Get industry distribution
    industries_result = db.execute(text("SELECT industry, COUNT(*) as count FROM contacts GROUP BY industry ORDER BY count DESC LIMIT 10"))
    industries_data = industries_result.fetchall()
    if industries_data:
        industries = [row[0] for row in industries_data]
        counts = [row[1] for row in industries_data]
        fig = px.bar(x=counts, y=industries, orientation='h', labels={'x': 'Count', 'y': 'Industry'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No industry data available")

with col2:
    st.subheader("🌍 Country Distribution")
    # Get country distribution
    countries_result = db.execute(text("SELECT country, COUNT(*) as count FROM contacts GROUP BY country ORDER BY count DESC LIMIT 10"))
    countries_data = countries_result.fetchall()
    if countries_data:
        countries = [row[0] for row in countries_data]
        counts = [row[1] for row in countries_data]
        fig = px.bar(x=counts, y=countries, orientation='h', labels={'x': 'Count', 'y': 'Country'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No country data available")

st.markdown("---")

# Trend Analysis
st.subheader("📈 Contact Growth Trend")
try:
    # Get contacts by month
    monthly_result = db.execute(text("""
        SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as count 
        FROM contacts 
        GROUP BY month 
        ORDER BY month DESC 
        LIMIT 12
    """))
    monthly_data = monthly_result.fetchall()
    
    if monthly_data:
        months = [row[0] for row in monthly_data]
        counts = [row[1] for row in monthly_data]
        
        fig = px.line(x=months, y=counts, labels={'x': 'Month', 'y': 'Number of Contacts'})
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No trend data available")
except Exception as e:
    st.info("Trend data not available")

st.markdown("---")

# Data Quality Metrics
st.subheader("🔍 Data Quality")
col1, col2, col3 = st.columns(3)

with col1:
    # Email completeness
    email_result = safe_db_execute(db, text("SELECT COUNT(*) as total, SUM(CASE WHEN email IS NOT NULL AND email != '' THEN 1 ELSE 0 END) as with_email FROM contacts"))
    email_data = email_result.fetchone()
    if email_data and email_data[0] > 0:
        email_pct = (email_data[1] / email_data[0]) * 100
        st.metric("Email Completeness", f"{email_pct:.1f}%")
    else:
        st.metric("Email Completeness", "0%")

with col2:
    # Phone completeness
    phone_result = safe_db_execute(db, text("SELECT COUNT(*) as total, SUM(CASE WHEN phone IS NOT NULL AND phone != '' THEN 1 ELSE 0 END) as with_phone FROM contacts"))
    phone_data = phone_result.fetchone()
    if phone_data and phone_data[0] > 0:
        phone_pct = (phone_data[1] / phone_data[0]) * 100
        st.metric("Phone Completeness", f"{phone_pct:.1f}%")
    else:
        st.metric("Phone Completeness", "0%")

with col3:
    # Company completeness
    company_result = safe_db_execute(db, text("SELECT COUNT(*) as total, SUM(CASE WHEN company IS NOT NULL AND company != '' THEN 1 ELSE 0 END) as with_company FROM contacts"))
    company_data = company_result.fetchone()
    if company_data and company_data[0] > 0:
        company_pct = (company_data[1] / company_data[0]) * 100
        st.metric("Company Completeness", f"{company_pct:.1f}%")
    else:
        st.metric("Company Completeness", "0%")

st.markdown("---")

# Top Companies
st.subheader("🏢 Top Companies")
top_companies_result = db.execute(text("""
    SELECT company, COUNT(*) as count 
    FROM contacts 
    WHERE company IS NOT NULL AND company != ''
    GROUP BY company 
    ORDER BY count DESC 
    LIMIT 10
"""))
top_companies_data = top_companies_result.fetchall()

if top_companies_data:
    companies = [row[0] for row in top_companies_data]
    counts = [row[1] for row in top_companies_data]
    
    fig = px.pie(values=counts, names=companies, title="Top Companies by Contact Count")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No company data available")

st.markdown("---")

# Summary Statistics
st.subheader("📋 Summary")
summary_data = []
summary_data.append({"Metric": "Total Contacts", "Value": stats['total']})
summary_data.append({"Metric": "Active Contacts", "Value": stats['active']})
summary_data.append({"Metric": "Unique Industries", "Value": stats['industries']})
summary_data.append({"Metric": "Unique Countries", "Value": stats['countries']})

st.table(summary_data)
