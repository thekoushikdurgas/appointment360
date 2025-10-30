"""
Accounts app URLs
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('password-reset/', views.password_reset_request, name='password-reset'),
    path('verify-email/', views.email_verify, name='verify-email'),
    
    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/picture/', views.profile_picture_upload, name='profile-picture-upload'),
]

