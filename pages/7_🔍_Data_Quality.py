"""
Data Quality Page
"""
import streamlit as st
import pandas as pd
from sqlalchemy import text
from config.database import get_db
from services.contact_service import ContactService
from components.sidebar import show_sidebar
from utils.custom_styles import apply_global_styles
from components.ui_components import hero_section

st.set_page_config(
    page_title="Data Quality - Contact Management System",
    page_icon="🔍",
    layout="wide"
)

# Apply global styles
apply_global_styles()

show_sidebar()

# Hero Section
hero_section("🔍 Data Quality", "Analyze and improve your data quality")

st.markdown("---")

# Initialize database
db = next(get_db())
contact_service = ContactService(db)

# Get statistics
stats = contact_service.get_contact_stats()

# Overall Quality Score
st.subheader("📊 Overall Quality Score")

# Calculate quality metrics
try:
    email_result = db.execute(text("SELECT COUNT(*) as total, SUM(CASE WHEN email IS NOT NULL AND email != '' THEN 1 ELSE 0 END) as with_email FROM contacts"))
    email_data = email_result.fetchone()
    email_pct = (email_data[1] / email_data[0]) * 100 if email_data and email_data[0] > 0 else 0
    
    phone_result = db.execute(text("SELECT COUNT(*) as total, SUM(CASE WHEN phone IS NOT NULL AND phone != '' THEN 1 ELSE 0 END) as with_phone FROM contacts"))
    phone_data = phone_result.fetchone()
    phone_pct = (phone_data[1] / phone_data[0]) * 100 if phone_data and phone_data[0] > 0 else 0
    
    company_result = db.execute(text("SELECT COUNT(*) as total, SUM(CASE WHEN company IS NOT NULL AND company != '' THEN 1 ELSE 0 END) as with_company FROM contacts"))
    company_data = company_result.fetchone()
    company_pct = (company_data[1] / company_data[0]) * 100 if company_data and company_data[0] > 0 else 0
    
    # Calculate weighted quality score
    quality_score = (email_pct * 0.4 + phone_pct * 0.3 + company_pct * 0.3)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display quality score with color
        if quality_score >= 80:
            color = "green"
            status = "Excellent"
        elif quality_score >= 60:
            color = "blue"
            status = "Good"
        elif quality_score >= 40:
            color = "orange"
            status = "Fair"
        else:
            color = "red"
            status = "Poor"
        
        st.markdown(f"<h1 style='color: {color}; text-align: center;'>{quality_score:.1f}%</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Status: <strong>{status}</strong></p>", unsafe_allow_html=True)
    
    with col2:
        # Progress bars for each metric
        st.write("**Email Completeness:**")
        st.progress(email_pct / 100)
        st.write(f"  {email_pct:.1f}% - {email_data[1] if email_data else 0} / {email_data[0] if email_data else 0} contacts")
        
        st.write("**Phone Completeness:**")
        st.progress(phone_pct / 100)
        st.write(f"  {phone_pct:.1f}% - {phone_data[1] if phone_data else 0} / {phone_data[0] if phone_data else 0} contacts")
        
        st.write("**Company Completeness:**")
        st.progress(company_pct / 100)
        st.write(f"  {company_pct:.1f}% - {company_data[1] if company_data else 0} / {company_data[0] if company_data else 0} contacts")
    
except Exception as e:
    st.error(f"Error calculating quality score: {str(e)}")

st.markdown("---")

# Field Completeness
st.subheader("📋 Field Completeness Details")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Email Completeness", f"{email_pct:.1f}%")
    
    # Get duplicates
    duplicate_result = db.execute(text("SELECT email, COUNT(*) as count FROM contacts WHERE email IS NOT NULL AND email != '' GROUP BY email HAVING count > 1"))
    duplicates = duplicate_result.fetchall()
    st.write(f"**Duplicate Emails:** {len(duplicates)}")

with col2:
    st.metric("Phone Completeness", f"{phone_pct:.1f}%")
    
    # Get missing phones
    missing_phone_result = db.execute(text("SELECT COUNT(*) FROM contacts WHERE phone IS NULL OR phone = ''"))
    missing_phones = missing_phone_result.scalar()
    st.write(f"**Missing Phones:** {missing_phones or 0}")

with col3:
    st.metric("Company Completeness", f"{company_pct:.1f}%")
    
    # Get missing companies
    missing_company_result = db.execute(text("SELECT COUNT(*) FROM contacts WHERE company IS NULL OR company = ''"))
    missing_companies = missing_company_result.scalar()
    st.write(f"**Missing Companies:** {missing_companies or 0}")

st.markdown("---")

# Data Issues
st.subheader("🔍 Data Issues")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📧 Email Issues")
    email_issues = []
    
    # Check for invalid emails
    all_emails_result = db.execute(text("SELECT email FROM contacts WHERE email IS NOT NULL AND email != ''"))
    all_emails = [row[0] for row in all_emails_result.fetchall()]
    
    invalid_emails = sum(1 for email in all_emails if '@' not in email)
    email_issues.append(f"Invalid format: {invalid_emails}")
    
    # Missing emails
    missing_result = db.execute(text("SELECT COUNT(*) FROM contacts WHERE email IS NULL OR email = ''"))
    missing_emails = missing_result.scalar()
    email_issues.append(f"Missing: {missing_emails or 0}")
    
    if email_issues:
        for issue in email_issues:
            st.write(f"- {issue}")
    else:
        st.write("✅ No email issues")

with col2:
    st.markdown("#### 📱 Phone Issues")
    phone_issues = []
    
    # Missing phones
    missing_result = db.execute(text("SELECT COUNT(*) FROM contacts WHERE phone IS NULL OR phone = ''"))
    missing_phones = missing_result.scalar()
    phone_issues.append(f"Missing: {missing_phones or 0}")
    
    if phone_issues:
        for issue in phone_issues:
            st.write(f"- {issue}")
    else:
        st.write("✅ No phone issues")

st.markdown("---")

# Recommendations
st.subheader("💡 Recommendations")

recommendations = []

if email_pct < 80:
    recommendations.append(f"📧 Improve email data quality: Currently at {email_pct:.1f}%")

if phone_pct < 80:
    recommendations.append(f"📱 Improve phone data quality: Currently at {phone_pct:.1f}%")

if company_pct < 80:
    recommendations.append(f"🏢 Improve company data quality: Currently at {company_pct:.1f}%")

if len(duplicates) > 0:
    recommendations.append(f"🔍 Review {len(duplicates)} duplicate email addresses")

if recommendations:
    for rec in recommendations:
        st.write(f"- {rec}")
else:
    st.success("✅ Data quality is excellent! No recommendations at this time.")

st.markdown("---")

# Quality Trends
st.subheader("📈 Quality Trends")
st.info("Quality trend tracking will be available after more data is collected")

# Export Quality Report
st.markdown("---")
if st.button("📥 Export Quality Report"):
    report_data = {
        'Metric': ['Overall Quality', 'Email Completeness', 'Phone Completeness', 'Company Completeness', 'Duplicate Emails', 'Missing Emails', 'Missing Phones', 'Missing Companies'],
        'Value': [f"{quality_score:.1f}%", f"{email_pct:.1f}%", f"{phone_pct:.1f}%", f"{company_pct:.1f}%", 
                 str(len(duplicates)), str(missing_emails or 0), str(missing_phones or 0), str(missing_companies or 0)]
    }
    
    report_df = pd.DataFrame(report_data)
    csv_data = report_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Quality Report",
        data=csv_data,
        file_name="data_quality_report.csv",
        mime="text/csv"
    )
