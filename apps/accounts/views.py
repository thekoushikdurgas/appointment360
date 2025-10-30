"""
Accounts views for login, logout, signup, and profile management
"""
import logging
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from supabase import create_client
from django.conf import settings
from services.supabase_storage_service import get_storage_service

logger = logging.getLogger(__name__)
User = get_user_model()

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login view with Supabase authentication"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        if email and password:
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                
                # Handle "remember me" with extended session
                if remember:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(3600)  # 1 hour
                
                messages.success(request, 'Login successful!')
                next_url = request.GET.get('next', 'core:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.warning(request, 'Please fill in all fields')
    
    return render(request, 'accounts/login.html')

@require_http_methods(["POST", "GET"])
def logout_view(request):
    """Logout view - properly clear Supabase session"""
    # Sign out from Supabase (best-effort)
    try:
        if settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY:
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
            access = request.session.get('supabase_access_token')
            refresh = request.session.get('supabase_refresh_token')
            if access and refresh:
                supabase.auth.set_session(access, refresh)
            supabase.auth.sign_out()
    except Exception as e:
        logger.warning(f"Supabase sign out failed: {e}")
    # Clear Supabase session tokens
    if 'supabase_access_token' in request.session:
        del request.session['supabase_access_token']
    if 'supabase_refresh_token' in request.session:
        del request.session['supabase_refresh_token']
    if 'supabase_user_id' in request.session:
        del request.session['supabase_user_id']
    if 'supabase_token_expires_at' in request.session:
        del request.session['supabase_token_expires_at']
    
    # Django logout
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('accounts:login')

@require_http_methods(["GET", "POST"])
def signup_view(request):
    """Signup view with Supabase authentication"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
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
            errors.append("Passwords do not match")
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                # Create user in Supabase
                if settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY:
                    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
                    
                    response = supabase.auth.sign_up({
                        "email": email,
                        "password": password,
                        "options": {
                            "data": {
                                "first_name": first_name or "",
                                "last_name": last_name or ""
                            },
                            "email_redirect_to": f"{request.scheme}://{request.get_host()}/accounts/verify-email/"
                        }
                    })
                    
                    if response.user:
                        # Check if user already exists
                        try:
                            existing_user = User.objects.get(email=email)
                            messages.error(request, 'An account with this email already exists. Please login instead.')
                            logger.warning(f"Signup attempted with existing email: {email}")
                            return render(request, 'accounts/signup.html')
                        except User.DoesNotExist:
                            pass
                        
                        # Create user in Django database
                        try:
                            user, created = User.objects.get_or_create(
                                supabase_user_id=response.user.id,
                                defaults={
                                    'email': email,
                                    'supabase_email': email,
                                    'username': email,
                                    'first_name': first_name or '',
                                    'last_name': last_name or '',
                                    'is_active': True,
                                    'email_verified': False,
                                }
                            )
                            
                            if created:
                                messages.success(
                                    request, 
                                    'Account created successfully! Please check your email to verify your account.'
                                )
                                logger.info(f"New user created: {email}")
                            else:
                                messages.info(request, 'Your account already exists. Please login.')
                                logger.info(f"User already exists: {email}")
                            
                            return redirect('accounts:login')
                        except IntegrityError as e:
                            logger.error(f"Integrity error during signup for {email}: {e}")
                            messages.error(request, 'Failed to create account. Please try again or contact support.')
                    else:
                        messages.error(request, 'Failed to create account in Supabase')
                        logger.error(f"Failed to create Supabase user for {email}")
            except Exception as e:
                logger.error(f"Signup error: {str(e)}")
                messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'accounts/signup.html')


@require_http_methods(["GET", "POST"])
def password_reset_request(request):
    """Password reset request view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            try:
                supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
                supabase.auth.reset_password_for_email(
                    email,
                    {"redirect_to": f"{request.scheme}://{request.get_host()}/accounts/password-reset/"}
                )
                messages.success(
                    request, 
                    'Password reset link sent! Please check your email.'
                )
                return redirect('accounts:login')
            except Exception as e:
                logger.error(f"Password reset error: {str(e)}")
                messages.error(request, 'Error sending password reset email')
    
    return render(request, 'accounts/password_reset.html')


@require_http_methods(["GET"])
def email_verify(request):
    """Email verification confirmation page"""
    token = request.GET.get('token')
    type = request.GET.get('type')
    
    if type == 'signup' and token:
        messages.success(request, 'Email verified successfully! You can now login.')
    elif type == 'recovery' and token:
        # This is handled by password reset
        pass
    
    return render(request, 'accounts/email_verify.html')


@login_required
@require_http_methods(["GET", "POST"])
def profile_view(request):
    """User profile view with picture upload"""
    if request.method == 'POST':
        # Update profile information
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', '')
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html')


@login_required
@require_http_methods(["POST"])
def profile_picture_upload(request):
    """Upload profile picture to Supabase Storage"""
    if 'profile_picture' in request.FILES:
        try:
            file = request.FILES['profile_picture']
            storage_service = get_storage_service()
            
            # Validate file
            is_valid, error_msg = storage_service.validate_file(
                file,
                allowed_types=['image/jpeg', 'image/jpg', 'image/png', 'image/webp'],
                max_size=5 * 1024 * 1024  # 5MB
            )
            
            if not is_valid:
                messages.error(request, error_msg)
                return redirect('accounts:profile')
            
            # Upload to Supabase Storage
            user = request.user
            file_path = f"profiles/{user.supabase_user_id}/{file.name}"
            
            # Delete old profile picture if exists
            if user.profile_picture:
                try:
                    storage_service.delete_file(user.profile_picture.split('/')[-1])
                except:
                    pass
            
            # Upload new profile picture
            public_url = storage_service.upload_file(
                file,
                file_path,
                bucket='user-uploads'
            )
            
            # Update user profile
            user.profile_picture = public_url
            user.save()
            
            messages.success(request, 'Profile picture updated successfully!')
            
        except Exception as e:
            logger.error(f"Profile picture upload error: {str(e)}")
            messages.error(request, f'Error uploading profile picture: {str(e)}')
    
    return redirect('accounts:profile')

