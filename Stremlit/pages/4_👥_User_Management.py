"""
User Management Page
"""
import streamlit as st
import pandas as pd
from config.database import get_db
from models.user import User, UserRole
from components.sidebar import show_sidebar
from utils.validators import validate_email
from utils.custom_styles import apply_global_styles
from components.ui_components import hero_section
import bcrypt

st.set_page_config(
    page_title="User Management - Contact Management System",
    page_icon="👥",
    layout="wide"
)

# Apply global styles
apply_global_styles()

show_sidebar()

# Hero Section
hero_section("👥 User Management", "Manage user accounts and permissions")

st.markdown("---")

# Initialize database
db = next(get_db())

# Modal state management
if 'show_add_user' not in st.session_state:
    st.session_state.show_add_user = False
if 'show_edit_user' not in st.session_state:
    st.session_state.show_edit_user = False
if 'edit_user_id' not in st.session_state:
    st.session_state.edit_user_id = None

# Get all users
users = db.query(User).all()

# Actions
col1, col2, col3 = st.columns([1, 1, 3])

with col1:
    if st.button("➕ Add User", width='stretch'):
        st.session_state.show_add_user = True
        st.rerun()

with col2:
    if st.button("🔄 Refresh", width='stretch'):
        st.rerun()

st.markdown("---")

# Display users
if users:
    # Create dataframe
    users_data = []
    for u in users:
        users_data.append({
            'ID': u.id,
            'Email': u.email,
            'First Name': u.first_name or '',
            'Last Name': u.last_name or '',
            'Role': u.role,
            'Active': '✅' if u.is_active else '❌',
            'Created': u.created_at.strftime("%Y-%m-%d") if u.created_at else ''
        })
    
    df = pd.DataFrame(users_data)
    st.dataframe(df, width='stretch', height=400)
    
    # Edit buttons
    st.markdown("#### Action Buttons")
    cols = st.columns(len(users) if len(users) <= 5 else 5)
    
    for idx, user in enumerate(users[:5]):
        with cols[idx]:
            if st.button(f"✏️ Edit {user.id}", key=f"edit_user_{user.id}", width='stretch'):
                st.session_state.show_edit_user = True
                st.session_state.edit_user_id = user.id
                st.rerun()
else:
    st.info("No users found. Add your first user!")

# Add User Form
if st.session_state.show_add_user:
    with st.container():
        st.markdown("---")
        st.subheader("➕ Add New User")
        
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                email = st.text_input("Email *")
                password = st.text_input("Password *", type="password")
                confirm_password = st.text_input("Confirm Password *", type="password")
            
            with col2:
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                role = st.selectbox("Role", [UserRole.ADMIN.value, UserRole.USER.value, UserRole.MANAGER.value])
                is_active = st.checkbox("Active", value=True)
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                submitted = st.form_submit_button("Save User", type="primary")
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submitted:
                errors = []
                if not email:
                    errors.append("Email is required")
                elif not validate_email(email):
                    errors.append("Invalid email format")
                elif db.query(User).filter(User.email == email).first():
                    errors.append("Email already exists")
                if not password or len(password) < 6:
                    errors.append("Password must be at least 6 characters")
                if password != confirm_password:
                    errors.append("Passwords do not match")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    try:
                        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        new_user = User(
                            email=email,
                            password_hash=password_hash,
                            first_name=first_name or None,
                            last_name=last_name or None,
                            role=role,
                            is_active=is_active
                        )
                        db.add(new_user)
                        db.commit()
                        st.success(f"✅ User '{email}' created successfully!")
                        st.session_state.show_add_user = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating user: {str(e)}")
            
            if cancel:
                st.session_state.show_add_user = False
                st.rerun()

# Edit User Form
if st.session_state.show_edit_user and st.session_state.edit_user_id:
    user_to_edit = db.query(User).filter(User.id == st.session_state.edit_user_id).first()
    
    if user_to_edit:
        with st.container():
            st.markdown("---")
            st.subheader(f"✏️ Edit User: {user_to_edit.email}")
            
            with st.form("edit_user_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    email = st.text_input("Email *", value=user_to_edit.email)
                    new_password = st.text_input("New Password (leave blank to keep current)", type="password")
                
                with col2:
                    first_name = st.text_input("First Name", value=user_to_edit.first_name or '')
                    last_name = st.text_input("Last Name", value=user_to_edit.last_name or '')
                    role = st.selectbox("Role", [UserRole.ADMIN.value, UserRole.USER.value, UserRole.MANAGER.value], 
                                      index=[UserRole.ADMIN.value, UserRole.USER.value, UserRole.MANAGER.value].index(user_to_edit.role))
                    is_active = st.checkbox("Active", value=user_to_edit.is_active)
                
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    submitted = st.form_submit_button("Update User", type="primary")
                with col2:
                    cancel = st.form_submit_button("Cancel")
                with col3:
                    delete = st.form_submit_button("Delete User", use_container_width=True)
                
                if submitted:
                    errors = []
                    if not email:
                        errors.append("Email is required")
                    elif not validate_email(email):
                        errors.append("Invalid email format")
                    elif email != user_to_edit.email:
                        if db.query(User).filter(User.email == email).first():
                            errors.append("Email already exists")
                    if new_password and len(new_password) < 6:
                        errors.append("New password must be at least 6 characters")
                    
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        try:
                            user_to_edit.email = email
                            user_to_edit.first_name = first_name or None
                            user_to_edit.last_name = last_name or None
                            user_to_edit.role = role
                            user_to_edit.is_active = is_active
                            
                            if new_password:
                                password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                                user_to_edit.password_hash = password_hash
                            
                            db.commit()
                            st.success(f"✅ User '{email}' updated successfully!")
                            st.session_state.show_edit_user = False
                            st.session_state.edit_user_id = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error updating user: {str(e)}")
                
                if cancel:
                    st.session_state.show_edit_user = False
                    st.session_state.edit_user_id = None
                    st.rerun()
                
                if delete:
                    if st.session_state.edit_user_id == 1:
                        st.error("Cannot delete admin user")
                    else:
                        try:
                            db.delete(user_to_edit)
                            db.commit()
                            st.success(f"✅ User '{user_to_edit.email}' deleted successfully!")
                            st.session_state.show_edit_user = False
                            st.session_state.edit_user_id = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting user: {str(e)}")
    else:
        st.error("User not found")
        st.session_state.show_edit_user = False
        st.session_state.edit_user_id = None
