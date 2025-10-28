"""
Import Progress Page - Monitor background import jobs
"""
import streamlit as st
from config.database import get_db
from models.import_job import ImportJob
from services.background_job_service import BackgroundJobService
from components.sidebar import show_sidebar
from utils.custom_styles import apply_global_styles
from components.ui_components import hero_section
import time
import json

st.set_page_config(
    page_title="Import Progress - Contact Management System",
    page_icon="📊",
    layout="wide"
)

# Apply global styles
apply_global_styles()

show_sidebar()

# Hero Section
hero_section("📊 Import Progress", "Monitor your data import jobs in real-time")

st.markdown("---")

# Initialize services
db = next(get_db())
job_service = BackgroundJobService()

# Auto-refresh
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

# Get active job ID from session state or query parameter
job_id = st.query_params.get('job_id', None)
if job_id:
    try:
        job_id = int(job_id)
    except (ValueError, TypeError):
        job_id = None

# If no job_id from query params, check session state
if not job_id and 'current_job_id' in st.session_state:
    job_id = st.session_state.current_job_id

if not job_id:
    st.warning("⚠️ No import job specified. Please start an import first.")
    
    # Show recent jobs
    st.markdown("### Recent Import Jobs")
    recent_jobs = job_service.get_recent_jobs(limit=10)
    
    if recent_jobs:
        for job in recent_jobs:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**{job['filename']}**")
            with col2:
                status_color = {
                    'COMPLETED': '🟢',
                    'PROCESSING': '🟡',
                    'FAILED': '🔴',
                    'CANCELLED': '⚪'
                }.get(job['status'], '⚪')
                st.write(f"{status_color} {job['status']}")
            with col3:
                if job['total_rows']:
                    st.write(f"Progress: {job['progress_percentage']:.1f}%")
            with col4:
                if job['created_at']:
                    st.write(f"Created: {job['created_at'][:10]}")
    
    st.stop()

# Get job status
job_status = job_service.get_job_status(job_id)

if not job_status:
    st.error("❌ Import job not found")
    st.stop()

# Display job information
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📄 {job_status['filename']}")
    
    # Status badge
    status_emoji = {
        'COMPLETED': '🟢',
        'PROCESSING': '🟡',
        'FAILED': '🔴',
        'CANCELLED': '⚪',
        'PENDING': '🔵'
    }.get(job_status['status'], '⚪')
    
    st.write(f"**Status:** {status_emoji} {job_status['status']}")
    
with col2:
    if not job_status['is_complete']:
        if st.button("🛑 Cancel Job"):
            if job_service.cancel_job(job_id):
                st.success("Job cancelled successfully")
                st.rerun()

st.markdown("---")

# Progress bar
if job_status['total_rows'] > 0:
    progress = job_status['progress_percentage'] / 100
    st.progress(progress)
    st.write(f"**{job_status['progress_percentage']:.1f}%** complete ({job_status['processed_rows']:,} / {job_status['total_rows']:,} rows)")

st.markdown("---")

# Statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Rows", f"{job_status['total_rows']:,}")

with col2:
    st.metric("✅ Success", f"{job_status['success_count']:,}", 
              delta=None if not job_status['total_rows'] else 
              f"{job_status['success_count'] / job_status['total_rows'] * 100:.1f}%")

with col3:
    st.metric("❌ Errors", f"{job_status['error_count']:,}",
              delta=None if not job_status['total_rows'] else 
              f"{job_status['error_count'] / job_status['total_rows'] * 100:.1f}%")

with col4:
    st.metric("📋 Duplicates", f"{job_status['duplicate_count']:,}")

st.markdown("---")

# Batch Information
if job_status['total_batches'] > 0:
    st.write(f"**Processing:** Batch {job_status['current_batch']} of {job_status['total_batches']}")
    
    if job_status['processing_speed']:
        st.write(f"**Speed:** {job_status['processing_speed']:.0f} rows/second")
    
    if job_status['estimated_completion']:
        from datetime import datetime
        eta = datetime.fromtimestamp(job_status['estimated_completion'])
        st.write(f"**ETA:** {eta.strftime('%H:%M:%S')}")

st.markdown("---")

# Timeline
if job_status['started_at']:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Started:** {job_status['started_at']}")
    
    if job_status['completed_at']:
        with col2:
            st.write(f"**Completed:** {job_status['completed_at']}")
            
        # Calculate duration
        from datetime import datetime
        start = datetime.fromisoformat(job_status['started_at'])
        end = datetime.fromisoformat(job_status['completed_at'])
        duration = end - start
        
        st.write(f"**Duration:** {duration}")

# Auto-refresh for processing jobs
if job_status['status'] == 'PROCESSING':
    if time.time() - st.session_state.last_refresh > 2:
        st.session_state.last_refresh = time.time()
        st.rerun()

# Completion message
if job_status['status'] == 'COMPLETED':
    st.success(f"🎉 Import completed successfully! {job_status['success_count']:,} contacts imported.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📇 View Contacts"):
            st.switch_page("pages/2_📇_Contacts.py")
    
    with col2:
        if st.button("📥 Import Another File"):
            st.switch_page("pages/3_📤_Import_Contacts.py")

elif job_status['status'] == 'FAILED':
    st.error(f"❌ Import failed. Error: {job_status.get('error_log', 'Unknown error')}")
    
    if st.button("🔄 Try Again"):
        st.switch_page("pages/3_📤_Import_Contacts.py")

db.close()

