"""
Supabase Authentication Service
"""
import streamlit as st
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY
import time

# Initialize Supabase client
supabase: Client = None


def get_supabase_client() -> Client:
    """Get or create Supabase client"""
    global supabase
    if supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            st.error("Supabase credentials not configured. Please set SUPABASE_URL and SUPABASE_KEY in .env file.")
            return None
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase


def check_authentication():
    """Check if user is authenticated"""
    # Check session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        return False
    
    # Check session timeout
    if 'last_activity' in st.session_state:
        elapsed = time.time() - st.session_state.last_activity
        if elapsed > 3600:  # 1 hour timeout
            st.session_state.authenticated = False
            st.session_state.user = None
            return False
    
    # Update last activity time
    st.session_state.last_activity = time.time()
    return True


def show_login():
    """Display login form with modern styling"""
    # Centered login card
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            margin: 2rem 0;
            box-shadow: 0 8px 24px rgba(255, 107, 53, 0.2);
            text-align: center;
        ">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">📇</h1>
            <h2 style="color: white; margin: 0.5rem 0;">Contact Manager</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 0;">Welcome back</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("### 🔐 Login to Your Account")
            
            email = st.text_input("📧 Email Address", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            remember = st.checkbox("Remember me")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("Cancel", use_container_width=True)
            
            if submitted:
                if email and password:
                    if login_user(email, password, remember):
                        st.success("✅ Login successful!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.warning("⚠️ Please fill in all fields")
        
        st.markdown("---")
        
        if st.button("📝 Don't have an account? Sign up", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()


def show_signup():
    """Display signup form with modern styling"""
    # Centered signup card
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            margin: 2rem 0;
            box-shadow: 0 8px 24px rgba(255, 107, 53, 0.2);
            text-align: center;
        ">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">📇</h1>
            <h2 style="color: white; margin: 0.5rem 0;">Create Account</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 0;">Join Contact Manager today</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("signup_form"):
            st.markdown("### 📝 Create Your Account")
            
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("👤 First Name", placeholder="Enter your first name")
                email = st.text_input("📧 Email", placeholder="your.email@example.com")
                password = st.text_input("🔒 Password", type="password", placeholder="Choose a strong password")
            
            with col2:
                last_name = st.text_input("👤 Last Name", placeholder="Enter your last name")
                confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
            
            # Password strength indicator
            if password:
                strength = 0
                if len(password) >= 8:
                    strength += 1
                if any(c.isdigit() for c in password):
                    strength += 1
                if any(c.isupper() for c in password):
                    strength += 1
                if any(c.islower() for c in password):
                    strength += 1
                if any(c in '!@#$%^&*' for c in password):
                    strength += 1
                
                colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
                icons = ['🔴', '🟠', '🟡', '🟢', '✅']
                strength_label = ['Weak', 'Fair', 'Good', 'Strong', 'Very Strong']
                
                st.progress(strength / 5)
                st.markdown(f"Password strength: {icons[min(strength, 4)]} {strength_label[min(strength, 4)]}")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("✅ Sign Up", type="primary", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("Cancel", use_container_width=True)
            
            if submitted:
                errors = []
                if not first_name:
                    errors.append("First name is required")
                if not email:
                    errors.append("Email is required")
                if not password:
                    errors.append("Password is required")
                elif len(password) < 8:
                    errors.append("Password must be at least 8 characters")
                
                if password and confirm_password and password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    if create_user(email, password, first_name, last_name):
                        st.success("✅ Account created successfully!")
                        st.info("ℹ️ Please login with your credentials.")
                        time.sleep(2)
                        st.session_state.show_signup = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to create account. Email may already exist.")
        
        st.markdown("---")
        
        if st.button("🔐 Already have an account? Login", use_container_width=True):
            st.session_state.show_signup = False
            st.rerun()


def login_user(email: str, password: str, remember: bool = False) -> bool:
    """Login user with Supabase"""
    try:
        client = get_supabase_client()
        if not client:
            return False
        
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            st.session_state.authenticated = True
            st.session_state.user = response.user
            st.session_state.last_activity = time.time()
            return True
        return False
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False


def create_user(email: str, password: str, first_name: str = None, last_name: str = None) -> bool:
    """Create new user with Supabase"""
    try:
        client = get_supabase_client()
        if not client:
            return False
        
        response = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "first_name": first_name or "",
                    "last_name": last_name or ""
                }
            }
        })
        
        return response.user is not None
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return False


def logout_user():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    if 'last_activity' in st.session_state:
        del st.session_state.last_activity
