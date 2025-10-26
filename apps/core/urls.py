"""
URL configuration for core app
"""
from django.urls import path
from .views import welcome_view, privacy_policy_view, contact_frontend_view

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('policies/shipping/', privacy_policy_view, name='privacy_policy'),
    path('contact/', contact_frontend_view, name='contact_frontend'),
]
