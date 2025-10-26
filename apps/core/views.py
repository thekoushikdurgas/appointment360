"""
Core views for frontend pages
"""
from django.shortcuts import render


def welcome_view(request):
    """Welcome/landing page"""
    return render(request, 'welcome.html')


def privacy_policy_view(request):
    """Privacy/Policy page"""
    return render(request, 'policies/shipping.html')


def contact_frontend_view(request):
    """Public contact listing page"""
    return render(request, 'contact_frontend/index.html')
