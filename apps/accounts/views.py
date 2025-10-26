"""
Views for authentication and user management
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .serializers import LoginSerializer, AdminUserSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from .models import AdminUser
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Track login IP
        user.last_login_ip = request.META.get('REMOTE_ADDR')
        user.save(update_fields=['last_login_ip'])
        
        user_serializer = AdminUserSerializer(user)
        logger.info(f"User {user.email} logged in from {user.last_login_ip}")
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': user_serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint
    """
    logger.info(f"User {request.user.email} logged out")
    logout(request)
    return Response({
        'success': True,
        'message': 'Logout successful'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    """
    Request password reset
    """
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = AdminUser.objects.get(email=email, is_active=True)
            
            # Generate reset token
            token = default_token_generator.make_token(user)
            user.reset_token = token
            user.save(update_fields=['reset_token'])
            
            # Send email with reset link
            reset_link = f"{request.scheme}://{request.get_host()}/admin/reset-password/{token}/"
            
            
            html_message = render_to_string('emails/reset_password.html', {
                'reset_link': reset_link,
                'current_year': datetime.now().year
            })
            
            send_mail(
                subject='Password Reset Request - Appointment360',
                message='',  # Plain text version (empty for HTML-only)
                html_message=html_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            
            logger.info(f"Password reset requested for {email}")
            
            return Response({
                'success': True,
                'message': 'Password reset link sent to your email'
            })
        except AdminUser.DoesNotExist:
            # Don't reveal that email doesn't exist
            logger.warning(f"Password reset requested for non-existent email: {email}")
            return Response({
                'success': True,
                'message': 'If the email exists, a password reset link will be sent'
            })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """
    Confirm password reset
    """
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            user = AdminUser.objects.get(reset_token=token, is_active=True)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.reset_token = None
                user.save()
                
                logger.info(f"Password reset successful for {user.email}")
                
                return Response({
                    'success': True,
                    'message': 'Password reset successful'
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Invalid or expired token'
                }, status=status.HTTP_400_BAD_REQUEST)
        except AdminUser.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid or expired token'
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get current user profile
    """
    serializer = AdminUserSerializer(request.user)
    return Response(serializer.data)


# Template-based views for web interface
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from datetime import datetime


@require_http_methods(["GET", "POST"])
def login_view_web(request):
    """
    Web-based login view
    """
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        if email and password:
            try:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    if not user.is_active:
                        messages.error(request, 'Your account is inactive.')
                        return redirect('accounts:login')
                    
                    # Track login IP
                    user.last_login_ip = request.META.get('REMOTE_ADDR')
                    user.save(update_fields=['last_login_ip'])
                    
                    # Login user
                    login(request, user)
                    
                    # Handle remember me
                    if not remember_me:
                        request.session.set_expiry(0)
                    
                    logger.info(f"User {user.email} logged in from {user.last_login_ip}")
                    messages.success(request, 'Login successful!')
                    
                    # Redirect to next or dashboard
                    next_url = request.GET.get('next', 'dashboard:index')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Invalid email or password.')
            except Exception as e:
                logger.error(f"Login error: {str(e)}")
                messages.error(request, 'An error occurred during login.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'admin/auth/login.html')


@login_required
def logout_view_web(request):
    """
    Web-based logout view
    """
    logger.info(f"User {request.user.email} logged out")
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@require_http_methods(["GET", "POST"])
def forgot_password_web(request):
    """
    Web-based forgot password view
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            try:
                user = AdminUser.objects.get(email=email, is_active=True)
                
                # Generate reset token
                token = default_token_generator.make_token(user)
                user.reset_token = token
                user.save(update_fields=['reset_token'])
                
                # Send email with reset link
                reset_link = f"{request.scheme}://{request.get_host()}/admin/reset-password/{token}/"
                
                
                html_message = render_to_string('emails/reset_password.html', {
                    'reset_link': reset_link,
                    'current_year': datetime.now().year
                })
                
                send_mail(
                    subject='Password Reset Request - Appointment360',
                    message='',  # Plain text version (empty for HTML-only)
                    html_message=html_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                
                logger.info(f"Password reset requested for {email}")
                messages.success(request, 'If the email exists, a password reset link will be sent.')
                return redirect('accounts:forgot_password')
            except AdminUser.DoesNotExist:
                # Don't reveal that email doesn't exist
                logger.warning(f"Password reset requested for non-existent email: {email}")
                messages.success(request, 'If the email exists, a password reset link will be sent.')
                return redirect('accounts:forgot_password')
        else:
            messages.error(request, 'Please enter your email address.')
    
    return render(request, 'admin/auth/forgot_password.html')


@require_http_methods(["GET", "POST"])
def reset_password_web(request, token):
    """
    Web-based password reset confirmation view
    """
    try:
        user = AdminUser.objects.get(reset_token=token, is_active=True)
        
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('password_confirmation')
            
            if new_password and confirm_password:
                if new_password != confirm_password:
                    messages.error(request, 'Passwords do not match.')
                    return render(request, 'admin/auth/reset_password.html', {'token': token})
                
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.reset_token = None
                    user.save()
                    
                    logger.info(f"Password reset successful for {user.email}")
                    messages.success(request, 'Password reset successful. Please login.')
                    return redirect('accounts:login')
                else:
                    messages.error(request, 'Invalid or expired token.')
                    return redirect('accounts:forgot_password')
            else:
                messages.error(request, 'Please fill in all fields.')
        
        return render(request, 'admin/auth/reset_password.html', {'token': token})
    except AdminUser.DoesNotExist:
        messages.error(request, 'Invalid or expired token.')
        return redirect('accounts:forgot_password')


@login_required
def profile_view(request):
    """
    Web-based profile view
    """
    from .forms import ProfileUpdateForm, CustomPasswordChangeForm
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'profile':
            form = ProfileUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('accounts:profile')
        elif form_type == 'password':
            form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    password_form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'admin/profile/edit.html', {
        'form': form,
        'password_form': password_form
    })


def send_authentication_alert_email(user, ip_address, browser):
    """
    Send email alert for new authentication/login
    """
    try:
        html_message = render_to_string('emails/new_authentication.html', {
            'account_email': user.email,
            'login_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip_address': ip_address,
            'browser': browser,
            'current_year': datetime.now().year
        })
        
        send_mail(
            subject='New Device Login Alert - Appointment360',
            message='',  # Plain text version (empty for HTML-only)
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,  # Fail silently to not disrupt login process
        )
    except Exception as e:
        logger.warning(f"Failed to send authentication alert email to {user.email}: {str(e)}")