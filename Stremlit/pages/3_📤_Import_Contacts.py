"""
Import Contacts Page - Upload and process CSV files
"""
import streamlit as st
import pandas as pd
import os
import time
from config.database import get_db
from services.csv_service import CSVService
from services.csv_column_mapper import CSVColumnMapper
from services.contact_service import ContactService
from models.contact import Contact
from services.import_error_tracker import ImportErrorTracker
from services.background_job_service import BackgroundJobService
from services.spark_import_service import SparkImportService
from services.file_validator import FileValidator
from config.settings import DATA_FOLDER_PATH
from components.sidebar import show_sidebar
from utils.custom_styles import apply_global_styles
from components.ui_components import hero_section
from pathlib import Path
from services.type_converter import TypeConverter

st.set_page_config(
    page_title="Import Contacts - Contact Management System",
    page_icon="📤",
    layout="wide"
)

# Apply global styles
apply_global_styles()

show_sidebar()

# Hero Section
hero_section("📤 Import Contacts", "Import contacts from CSV files into your database")

st.markdown("---")

# Tabs for different import methods
tab1, tab2 = st.tabs(["📤 Upload File", "📁 Local File"])

# Initialize services
db = next(get_db())
csv_service = CSVService()
mapper = CSVColumnMapper()
contact_service = ContactService(db)
error_tracker = ImportErrorTracker()
background_job_service = BackgroundJobService()
spark_import_service = SparkImportService()

# Handle selected file path
selected_file_path = None
filename = None

with tab1:
    st.subheader("Upload CSV File")
    uploaded_file = st.file_uploader(
        "Choose a CSV file to upload",
        type=['csv'],
        help="Upload a CSV file containing contact information"
    )
    
    if uploaded_file is not None:
        # Save file temporarily
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_file_path = f"/tmp/{uploaded_file.name}"
        
        # Create temp directory if it doesn't exist
        os.makedirs("/tmp", exist_ok=True)
        
        # Save uploaded file
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        selected_file_path = temp_file_path
        filename = uploaded_file.name

with tab2:
    st.subheader("Import from Local File")
    
    # Dropdown for files in data folder
    csv_files = FileValidator.list_csv_files(DATA_FOLDER_PATH)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if csv_files:
            file_options = [Path(f).name for f in csv_files]
            selected_dropdown = st.selectbox(
                "Select a file from data folder:",
                [""] + file_options
            )
            
            if selected_dropdown:
                selected_file_path = os.path.join(DATA_FOLDER_PATH, selected_dropdown)
                filename = selected_dropdown
    
    with col2:
        st.markdown("**OR**")
        manual_path = st.text_input(
            "Enter absolute file path:",
            help="Enter the full path to your CSV file"
        )
        
        if manual_path:
            selected_file_path = manual_path
            filename = os.path.basename(manual_path)

# Process file if one was selected
if selected_file_path and filename:
    # Validate file path
    is_valid, error_msg = FileValidator.validate_local_path(selected_file_path)
    
    if not is_valid:
        st.error(f"❌ {error_msg}")
    else:
        # Get file size
        file_size_mb = FileValidator.get_file_size_mb(selected_file_path)
        st.success(f"✅ File selected: {filename} ({file_size_mb:.2f} MB)")
        
        # Check if we should use PySpark for large files
        use_pyspark = file_size_mb > 10  # 10MB threshold
        
        if use_pyspark and spark_import_service.is_available():
            # Use PySpark for large file imports
            st.info("🚀 Large file detected. Using PySpark for optimized processing.")
            
            # Show preview using PySpark
            preview_df = spark_import_service.get_preview(selected_file_path, num_rows=10)
            
            if preview_df:
                st.subheader("📋 CSV Preview (first 10 rows)")
                st.dataframe(preview_df.toPandas(), width='stretch')
            
            st.write(f"**File Size:** {file_size_mb:.2f} MB")
            
            # Column Mapping
            st.subheader("🗺️ Column Mapping")
            
            # Auto-detect mappings from preview
            df_pandas = preview_df.toPandas() if preview_df is not None else None
            
            if df_pandas is not None:
                auto_mapping = mapper.auto_map_columns(df_pandas)
                
                if auto_mapping:
                    st.success(f"✅ Auto-detected {len(auto_mapping)} column mappings")
                    
                    # Display mapping
                    st.write("**Mapped Columns:**")
                    for csv_col, db_field in auto_mapping.items():
                        st.write(f"- `{csv_col}` → `{db_field}`")
                else:
                    st.warning("⚠️ Could not auto-detect column mappings")
            
            st.markdown("---")
            
            # Import button
            if st.button("🚀 Start Import", type="primary", width='stretch', key='import_btn_large'):
                # Get user ID
                user_id = 1
                if 'user' in st.session_state and st.session_state.user:
                    user_id = getattr(st.session_state.user, 'id', 1)
                
                # Create background job
                job = background_job_service.create_import_job(
                    db, filename, selected_file_path, auto_mapping, user_id
                )
                
                # Start background import
                background_job_service.start_import_job(job.id, selected_file_path, auto_mapping)
                
                st.success(f"✅ Import job #{job.id} started in background!")
                st.info("📊 Redirecting to progress page...")
                
                # Store job_id in session state for navigation
                st.session_state.current_job_id = job.id
                
                # Redirect to progress page
                time.sleep(2)
                st.switch_page("pages/9_📊_Import_Progress.py")
        
        else:
            # Use traditional Pandas for small files
            # Read CSV
            df = csv_service.read_csv_file(selected_file_path)
            
            if df is not None:
                # Show preview
                st.subheader("📋 CSV Preview")
                st.dataframe(df.head(10), width='stretch')
                
                st.write(f"**Total Rows:** {len(df)}")
                st.write(f"**Total Columns:** {len(df.columns)}")
                
                st.markdown("---")
                
                # Column Mapping
                st.subheader("🗺️ Column Mapping")
                
                # Auto-detect mappings
                auto_mapping = mapper.auto_map_columns(df)
                
                if auto_mapping:
                    st.success(f"✅ Auto-detected {len(auto_mapping)} column mappings")
                    
                    # Display mapping
                    st.write("**Mapped Columns:**")
                    for csv_col, db_field in auto_mapping.items():
                        st.write(f"- `{csv_col}` → `{db_field}`")
                else:
                    st.warning("⚠️ Could not auto-detect column mappings")
                
                st.markdown("---")
                
                # Import button
                if st.button("🚀 Import Contacts", type="primary", width='stretch', key='import_btn_small'):
                    if not auto_mapping:
                        st.error("❌ Please configure column mappings first")
                    else:
                        # Process in chunks
                        chunks = csv_service.process_chunks(df, chunk_size=1000)
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        total_imported = 0
                        total_errors = 0
                        total_skipped = 0
                        
                        # Get user ID
                        user_id = 1
                        if 'user' in st.session_state and st.session_state.user:
                            user_id = getattr(st.session_state.user, 'id', 1)
                        
                        global_row_counter = 0
                        for i, chunk in enumerate(chunks):
                            status_text.write(f"Processing chunk {i+1}/{len(chunks)}...")
                            
                            for idx, row in chunk.iterrows():
                                try:
                                    global_row_counter += 1
                                    # Build contact data from mapping
                                    contact_data = {}
                                    
                                    for csv_col, db_field in auto_mapping.items():
                                        if csv_col in chunk.columns:
                                            value = row[csv_col]
                                            # Use type converter to properly handle numeric fields
                                            converted_value = TypeConverter.convert_value(db_field, value)
                                            contact_data[db_field] = converted_value
                                            
                                            # Debug: Log if annual_revenue is still a string
                                            if db_field == 'annual_revenue' and isinstance(converted_value, str):
                                                print(f"WARNING: annual_revenue is still string: {converted_value}")
                                    
                                    # Set user_id
                                    contact_data['user_id'] = user_id
                                    
                                    # Skip if email already exists
                                    email = contact_data.get('email')
                                    if email:
                                        existing = contact_service.get_contact_by_email(email)
                                        if existing:
                                            total_skipped += 1
                                            error_tracker.add_error(
                                                global_row_counter, 
                                                'email', 
                                                'Duplicate email found', 
                                                email
                                            )
                                            continue
                                    
                                    # Add contact (don't commit yet)
                                    contact = Contact(**contact_data)
                                    db.add(contact)
                                    total_imported += 1
                                    
                                    # Commit in batches of 100 to avoid memory issues
                                    if total_imported % 100 == 0:
                                        try:
                                            db.commit()
                                        except Exception as batch_error:
                                            db.rollback()
                                            raise batch_error
                                    
                                except Exception as e:
                                    total_errors += 1
                                    error_tracker.add_error(
                                        global_row_counter,
                                        'unknown',
                                        f"Error: {str(e)}",
                                        str(row.to_dict())
                                    )
                                    # Rollback any pending changes for this row
                                    try:
                                        db.rollback()
                                    except Exception as rollback_err:
                                        # If rollback fails, close and get new session
                                        try:
                                            db.close()
                                            db = next(get_db())
                                        except:
                                            pass
                                    # Skip to next row - don't attempt to continue
                                    continue
                            
                            progress_bar.progress((i + 1) / len(chunks))
                        
                        try:
                            # Commit remaining changes
                            db.commit()
                            status_text.write(f"✅ Import complete! {total_imported} contacts imported, {total_skipped} skipped, {total_errors} errors")
                        except Exception as commit_error:
                            try:
                                db.rollback()
                            except:
                                pass
                            status_text.write(f"❌ Error committing changes: {str(commit_error)}")
                            st.error(f"Import failed during commit: {str(commit_error)}")
                        
                        if total_imported > 0:
                            st.success(f"🎉 Successfully imported {total_imported} contacts!")
                        
                        if total_skipped > 0:
                            st.warning(f"⚠️ Skipped {total_skipped} duplicates")
                        
                        if total_errors > 0:
                            st.error(f"❌ {total_errors} errors occurred during import")
                        
                        # Show errors if any
                        if error_tracker.get_error_count() > 0:
                            st.markdown("---")
                            st.subheader("📊 Error Summary")
                            for error_type, count in error_tracker.get_error_summary().items():
                                st.write(f"- **{error_type}**: {count}")
                            
                            # Show detailed errors (first 10)
                            st.markdown("#### Detailed Errors (first 10)")
                            for error in error_tracker.get_errors()[:10]:
                                st.write(f"Row {error.row_number}, Column '{error.column}': {error.error_message}")
