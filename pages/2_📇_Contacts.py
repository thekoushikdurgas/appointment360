"""
Contacts Page - List and manage contacts
"""
import streamlit as st
import pandas as pd
from sqlalchemy import text
from config.database import get_db
from services.contact_service import ContactService
from services.csv_service import CSVService
from services.export_limit_service import ExportLimitService
from components.sidebar import show_sidebar
from utils.validators import validate_email, validate_phone, validate_url
from utils.custom_styles import apply_global_styles
from components.ui_components import hero_section

st.set_page_config(
    page_title="Contacts - Contact Management System",
    page_icon="📇",
    layout="wide"
)

# Apply global styles
apply_global_styles()

show_sidebar()

# Hero Section
hero_section("📇 Contacts", "Manage your contact database efficiently")

# Initialize services
db = next(get_db())
contact_service = ContactService(db)
csv_service = CSVService()
export_limit_service = ExportLimitService(db)

# Get user ID
user_id = 1
if 'user' in st.session_state and st.session_state.user:
    user_id = getattr(st.session_state.user, 'id', 1)

# Modal state management
if 'show_add_contact' not in st.session_state:
    st.session_state.show_add_contact = False
if 'show_edit_contact' not in st.session_state:
    st.session_state.show_edit_contact = False
if 'edit_contact_id' not in st.session_state:
    st.session_state.edit_contact_id = None
if 'selected_contacts' not in st.session_state:
    st.session_state.selected_contacts = []

# Check export limits
can_export, remaining = export_limit_service.check_limit(user_id)

# Enhanced Filters
st.markdown("### 🔍 Search & Filter")
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search = st.text_input("🔍 Search Contacts", 
                              placeholder="Name, company, email...", 
                              value=st.session_state.get('search_query', ''),
                              help="Search by name, company, or email")
    
    with col2:
        # Get unique industries from database
        industries_result = db.execute(text("SELECT DISTINCT industry FROM contacts WHERE industry IS NOT NULL"))
        industries = industries_result.fetchall()
        industry_options = [row[0] for row in industries] if industries else ["Technology", "Healthcare", "Finance", "Education"]
        industry_filter = st.multiselect("🏭 Industry", industry_options, help="Filter by industry")
    
    with col3:
        # Get unique countries from database
        countries_result = db.execute(text("SELECT DISTINCT country FROM contacts WHERE country IS NOT NULL"))
        countries = countries_result.fetchall()
        country_options = [row[0] for row in countries] if countries else ["United States", "United Kingdom", "Canada", "Australia"]
        country_filter = st.multiselect("🌍 Country", country_options, help="Filter by country")

# Store search query in session
st.session_state.search_query = search

# Action Buttons
st.markdown("### ⚡ Quick Actions")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("➕ Add Contact", use_container_width=True, type="primary"):
        st.session_state.show_add_contact = True
        st.rerun()

with col2:
    export_all_btn = st.button("📤 Export All", use_container_width=True, key='export_all')

with col3:
    export_filtered_btn = st.button("📤 Export Filtered", use_container_width=True, key='export_filtered')

with col4:
    if st.button("📥 Import CSV", use_container_width=True):
        st.switch_page("pages/3_📤_Import_Contacts.py")

with col5:
    st.metric("📊 Remaining", f"{remaining} exports")

st.markdown("---")

# Build filters
filters = {
    'search': search,
    'industry': industry_filter if industry_filter else None,
    'country': country_filter if country_filter else None
}

# Get contacts
page = st.number_input("Page", min_value=1, value=1)
result = contact_service.filter_contacts(filters, page=page, per_page=25)

# Display contacts
if result['contacts']:
    # Create dataframe with action column
    contacts_data = []
    for c in result['contacts']:
        contacts_data.append({
            'ID': c.id,
            'Name': c.full_name or '',
            'Company': c.company or '',
            'Email': c.email or '',
            'Phone': c.phone or '',
            'Industry': c.industry or '',
            'Country': c.country or '',
            'Created': c.created_at.strftime("%Y-%m-%d") if c.created_at else ''
        })
    
    df = pd.DataFrame(contacts_data)
    
    # Display with selection
    selected_indices = st.dataframe(
        df,
        width='stretch',
        height=400
    )
    
    # Action buttons for each row
    st.markdown("#### Action Buttons")
    col1, col2, col3, col4 = st.columns(4)
    
    for idx, contact in enumerate(result['contacts']):
        if idx < 4:  # Show for first 4 contacts in current page
            with col1 if idx == 0 else col2 if idx == 1 else col3 if idx == 2 else col4:
                if st.button(f"✏️ Edit {contact.id}", key=f"edit_{contact.id}", width='stretch'):
                    st.session_state.show_edit_contact = True
                    st.session_state.edit_contact_id = contact.id
                    st.rerun()
    
    # Pagination
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write(f"Page {result['page']} of {result['pages']} ({result['total']} total contacts)")
else:
    st.info("No contacts found. Import some contacts to get started!")

# Add Contact Modal
if st.session_state.show_add_contact:
    with st.container():
        st.markdown("---")
        st.subheader("➕ Add New Contact")
        
        with st.form("add_contact_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name *")
                last_name = st.text_input("Last Name")
                email = st.text_input("Email *")
                phone = st.text_input("Phone")
                company = st.text_input("Company")
                industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Education", "Other"])
            
            with col2:
                title = st.text_input("Job Title")
                website = st.text_input("Website")
                city = st.text_input("City")
                state = st.text_input("State")
                country = st.text_input("Country")
                linkedin = st.text_input("LinkedIn URL")
            
            notes = st.text_area("Notes")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                submitted = st.form_submit_button("Save Contact", type="primary")
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submitted:
                # Validation
                errors = []
                if not first_name:
                    errors.append("First name is required")
                if not email:
                    errors.append("Email is required")
                elif not validate_email(email):
                    errors.append("Invalid email format")
                if email and validate_email(email):
                    # Check for duplicate email
                    existing = contact_service.get_contact_by_email(email)
                    if existing:
                        errors.append("Email already exists")
                if phone and not validate_phone(phone):
                    errors.append("Invalid phone format")
                if website and not validate_url(website):
                    errors.append("Invalid website URL")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    try:
                        contact_data = {
                            'first_name': first_name,
                            'last_name': last_name or '',
                            'full_name': f"{first_name} {last_name or ''}".strip(),
                            'email': email,
                            'phone': phone or '',
                            'company': company or '',
                            'industry': industry or '',
                            'title': title or '',
                            'website': website or '',
                            'city': city or '',
                            'state': state or '',
                            'country': country or '',
                            'linkedin': linkedin or '',
                            'notes': notes or '',
                            'user_id': user_id
                        }
                        
                        new_contact = contact_service.create_contact(contact_data)
                        st.success(f"✅ Contact '{new_contact.full_name}' created successfully!")
                        st.session_state.show_add_contact = False
                        st.rerun()
                    except ValueError as e:
                        st.error(f"Validation error: {str(e)}")
                    except Exception as e:
                        st.error(f"Error creating contact: {str(e)}")
            
            if cancel:
                st.session_state.show_add_contact = False
                st.rerun()

# Edit Contact Modal
if st.session_state.show_edit_contact and st.session_state.edit_contact_id:
    contact_to_edit = contact_service.get_contact(st.session_state.edit_contact_id)
    
    if contact_to_edit:
        with st.container():
            st.markdown("---")
            st.subheader(f"✏️ Edit Contact: {contact_to_edit.full_name}")
            
            with st.form("edit_contact_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name *", value=contact_to_edit.first_name or '')
                    last_name = st.text_input("Last Name", value=contact_to_edit.last_name or '')
                    email = st.text_input("Email *", value=contact_to_edit.email or '')
                    phone = st.text_input("Phone", value=contact_to_edit.phone or '')
                    company = st.text_input("Company", value=contact_to_edit.company or '')
                    industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Education", "Other"], 
                                           index=["Technology", "Healthcare", "Finance", "Education", "Other"].index(contact_to_edit.industry) if contact_to_edit.industry in ["Technology", "Healthcare", "Finance", "Education", "Other"] else 0)
                
                with col2:
                    title = st.text_input("Job Title", value=contact_to_edit.title or '')
                    website = st.text_input("Website", value=contact_to_edit.website or '')
                    city = st.text_input("City", value=contact_to_edit.city or '')
                    state = st.text_input("State", value=contact_to_edit.state or '')
                    country = st.text_input("Country", value=contact_to_edit.country or '')
                    linkedin = st.text_input("LinkedIn URL", value=contact_to_edit.linkedin or '')
                
                notes = st.text_area("Notes", value=contact_to_edit.notes or '')
                is_active = st.checkbox("Active", value=contact_to_edit.is_active if hasattr(contact_to_edit, 'is_active') else True)
                
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    submitted = st.form_submit_button("Update Contact", type="primary")
                with col2:
                    cancel = st.form_submit_button("Cancel")
                with col3:
                    delete = st.form_submit_button("Delete Contact", use_container_width=True)
                
                if submitted:
                    errors = []
                    if not first_name:
                        errors.append("First name is required")
                    if not email:
                        errors.append("Email is required")
                    elif not validate_email(email):
                        errors.append("Invalid email format")
                    if email != contact_to_edit.email:
                        # Check for duplicate email
                        existing = contact_service.get_contact_by_email(email)
                        if existing:
                            errors.append("Email already exists")
                    if phone and not validate_phone(phone):
                        errors.append("Invalid phone format")
                    if website and not validate_url(website):
                        errors.append("Invalid website URL")
                    
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        try:
                            contact_data = {
                                'first_name': first_name,
                                'last_name': last_name or '',
                                'full_name': f"{first_name} {last_name or ''}".strip(),
                                'email': email,
                                'phone': phone or '',
                                'company': company or '',
                                'industry': industry or '',
                                'title': title or '',
                                'website': website or '',
                                'city': city or '',
                                'state': state or '',
                                'country': country or '',
                                'linkedin': linkedin or '',
                                'notes': notes or '',
                                'is_active': is_active
                            }
                            
                            updated_contact = contact_service.update_contact(st.session_state.edit_contact_id, contact_data)
                            if updated_contact:
                                st.success(f"✅ Contact '{updated_contact.full_name}' updated successfully!")
                                st.session_state.show_edit_contact = False
                                st.session_state.edit_contact_id = None
                                st.rerun()
                            else:
                                st.error("Failed to update contact")
                        except ValueError as e:
                            st.error(f"Validation error: {str(e)}")
                        except Exception as e:
                            st.error(f"Error updating contact: {str(e)}")
                
                if cancel:
                    st.session_state.show_edit_contact = False
                    st.session_state.edit_contact_id = None
                    st.rerun()
                
                if delete:
                    if contact_service.delete_contact(st.session_state.edit_contact_id):
                        st.success(f"✅ Contact '{contact_to_edit.full_name}' deleted successfully!")
                        st.session_state.show_edit_contact = False
                        st.session_state.edit_contact_id = None
                        st.rerun()
                    else:
                        st.error("Failed to delete contact")
    else:
        st.error("Contact not found")
        st.session_state.show_edit_contact = False
        st.session_state.edit_contact_id = None

# Handle export
if export_all_btn or export_filtered_btn:
    if not can_export:
        st.warning(f"⚠️ Export limit reached. {remaining} exports remaining.")
    else:
        try:
            # Get contacts to export
            if export_all_btn:
                filters_to_use = {'search': '', 'industry': None, 'country': None}
                result = contact_service.filter_contacts(filters_to_use, page=1, per_page=10000)
            else:
                result = contact_service.filter_contacts(filters, page=1, per_page=10000)
            
            if result['contacts']:
                # Prepare data
                export_data = []
                for c in result['contacts']:
                    export_data.append({
                        'ID': c.id,
                        'First Name': c.first_name or '',
                        'Last Name': c.last_name or '',
                        'Full Name': c.full_name or '',
                        'Email': c.email or '',
                        'Phone': c.phone or '',
                        'Company': c.company or '',
                        'Industry': c.industry or '',
                        'Title': c.title or '',
                        'Website': c.website or '',
                        'City': c.city or '',
                        'State': c.state or '',
                        'Country': c.country or '',
                        'LinkedIn': c.linkedin or '',
                        'Notes': c.notes or ''
                    })
                
                df_export = pd.DataFrame(export_data)
                
                # Export as CSV
                csv_data = csv_service.export_to_csv(df_export)
                
                # Log export
                export_limit_service.log_export(
                    user_id=user_id,
                    export_type="contacts",
                    export_format="csv",
                    record_count=len(export_data)
                )
                
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name="contacts_export.csv",
                    mime="text/csv"
                )
                st.success(f"✅ {len(export_data)} contacts exported")
            else:
                st.info("No contacts to export")
        except Exception as e:
            st.error(f"Export error: {str(e)}")
