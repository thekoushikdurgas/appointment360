"""
URL configuration for accounts app
"""
from django.urls import path
from .views import (
    login_view, logout_view, password_reset, password_reset_confirm, profile,
    login_view_web, logout_view_web, forgot_password_web, reset_password_web, profile_view
)

app_name = 'accounts'

urlpatterns = [
    # API endpoints
    path('api/auth/login/', login_view, name='api-login'),
    path('api/auth/logout/', logout_view, name='api-logout'),
    path('api/auth/password-reset/', password_reset, name='api-password-reset'),
    path('api/auth/password-reset-confirm/', password_reset_confirm, name='api-password-reset-confirm'),
    path('api/auth/profile/', profile, name='api-profile'),
    
    # Web-based views
    path('admin/login/', login_view_web, name='login'),
    path('admin/logout/', logout_view_web, name='logout'),
    path('admin/forgot-password/', forgot_password_web, name='forgot_password'),
    path('admin/reset-password/<str:token>/', reset_password_web, name='reset_password'),
    path('admin/profile/', profile_view, name='profile'),
]

