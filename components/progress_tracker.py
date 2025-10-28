"""
Progress Tracker Component
"""
import streamlit as st
from datetime import datetime


def show_progress_tracker():
    """Display progress tracker with checkboxes"""
    st.sidebar.header("📊 Implementation Progress")
    
    # Task list organized by phase with detailed checkboxes
    tasks = {
        # Phase 1: Complete
        'setup-project': ('✅ Initialize project structure', True),
        'setup-database': ('✅ Set up database and models', True),
        'implement-auth': ('✅ Build authentication system', True),
        
        # Phase 2: Core Features
        'build-dashboard': ('✅ Create dashboard with charts', True),
        'contact-service': ('✅ Implement contact CRUD service', True),
        'filter-system': ('✅ Build advanced filtering', True),
        'contacts-page': ('✅ Create contacts page', True),
        
        # CSV Import - Detailed tasks
        'csv-import-basic': ('✅ CSV import basic functionality', True),
        'csv-import-chunks': ('✅ Chunked processing for large files', True),
        'csv-import-progress': ('✅ Progress indicators for imports', True),
        'csv-import-validation': ('✅ Basic validation and duplicate detection', True),
        'csv-import-mapping': ('✅ Advanced column mapping UI', True),
        'csv-import-errors': ('✅ Enhanced error tracking and reporting', True),
        'csv-import-duplicates': ('📤 Advanced fuzzy duplicate detection', False),
        'csv-import-transforms': ('📤 Data transformation pipeline', False),
        
        # CSV Export - Detailed tasks
        'export-basic': ('✅ Basic Excel/CSV export', True),
        'export-ui': ('✅ Export UI and buttons', True),
        'export-selected': ('✅ Export selected contacts', True),
        'export-format-selector': ('✅ Export format selector (Excel/CSV)', True),
        'export-options': ('✅ Export all/filtered/current page options', True),
        'export-all-filtered': ('✅ Export all contacts functionality', True),
        'export-limits': ('✅ Implement download limits', True),
        'export-tracking': ('✅ Export history and tracking', True),
        'export-templates': ('📥 Export templates', False),
        'export-enhancements': ('📥 Excel formatting and multi-sheet', False),
        
        # User & Settings
        'user-management': ('✅ User management page', True),
        'settings-page': ('✅ Settings page', True),
        
        # Phase 3: PySpark (Complete)
        'pyspark-setup': ('✅ PySpark environment setup', True),
        'spark-services': ('✅ Core Spark services', True),
        'spark-csv-import': ('✅ Large-scale import', True),
        'spark-analytics': ('✅ Analytics service', True),
        'data-quality': ('✅ Data quality service', True),
        'deduplication': ('✅ Deduplication service', True),
        
        # Phase 4: Analytics (Complete)
        'analytics-page': ('✅ Analytics dashboard', True),
        'data-quality-page': ('✅ Data quality interface', True),
        'export-history-page': ('✅ Export history page', True),
        
        # Phase 5: Testing
        'unit-tests-core': ('✅ Basic unit tests', True),
        'unit-tests-spark': ('🧪 Spark service tests', False),
        'unit-tests-export': ('✅ Export service tests', True),
        'unit-tests-column-mapper': ('✅ Column mapper tests', True),
        'unit-tests-error-tracker': ('✅ Error tracker tests', True),
        'integration-tests': ('🧪 Integration tests', False),
        'performance-tests': ('🧪 Performance tests', False),
        'security-tests': ('🧪 Security tests', False),
        
        # Phase 6: Performance
        'db-optimization': ('✅ Database optimization and indexes', True),
        'spark-optimization': ('⚡ Spark configuration', False),
        'app-performance': ('⚡ App performance', False),
        
        # Phase 7: Documentation
        'doc-user': ('📚 User documentation', False),
        'doc-developer': ('📚 Developer documentation', False),
        
        # Phase 8: UI/UX
        'ui-polish': ('🎨 UI/UX polish', False)
    }
    
    # Initialize progress state
    if 'progress' not in st.session_state:
        st.session_state.progress = {}
        for task_id, (_, default_complete) in tasks.items():
            st.session_state.progress[task_id] = default_complete
    else:
        for task_id, (_, default_complete) in tasks.items():
            if task_id not in st.session_state.progress:
                st.session_state.progress[task_id] = default_complete
    
    # Calculate progress by phase
    phase_stats = {
        'Phase 1 - Foundation': {'total': 3, 'completed': 3},
        'Phase 2 - Core Features': {'total': 22, 'completed': 20},
        'Phase 3 - PySpark': {'total': 6, 'completed': 6},
        'Phase 4 - Analytics': {'total': 3, 'completed': 3},
        'Phase 5 - Testing': {'total': 8, 'completed': 4},
        'Phase 6 - Performance': {'total': 3, 'completed': 1},
        'Phase 7 - Documentation': {'total': 2, 'completed': 0},
        'Phase 8 - UI Polish': {'total': 1, 'completed': 0}
    }
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task_id in tasks.keys() if st.session_state.progress.get(task_id, False))
    progress_percentage = (completed_tasks / total_tasks) * 100
    
    # Enhanced progress bar
    st.sidebar.markdown("""
    <div style="
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(255, 107, 53, 0.2);
        color: white;
    ">
        <p style="margin: 0; font-weight: 600; text-align: center;">
            Overall Progress: {:.0f}%
        </p>
        <p style="margin: 0.5rem 0 0 0; text-align: center; font-size: 0.85rem; opacity: 0.9;">
            {}/{} tasks completed
        </p>
    </div>
    """.format(progress_percentage, completed_tasks, total_tasks), unsafe_allow_html=True)
    
    st.sidebar.progress(progress_percentage / 100)
    
    st.sidebar.markdown("---")
    
    # Phase-by-phase progress
    st.sidebar.subheader("Phase Progress:")
    for phase_name, stats in phase_stats.items():
        completed = stats['completed']
        total = stats['total']
        phase_percentage = (completed / total * 100) if total > 0 else 0
        status_icon = "✅" if completed == total else "🚧"
        st.sidebar.caption(f"{status_icon} {phase_name}: {completed}/{total} ({phase_percentage:.0f}%)")
    
    st.sidebar.markdown("---")
    st.sidebar.caption(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")


def update_task_progress(task_id: str, completed: bool):
    """Update task progress"""
    if 'progress' not in st.session_state:
        st.session_state.progress = {}
    st.session_state.progress[task_id] = completed
