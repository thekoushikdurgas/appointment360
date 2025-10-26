"""
Dashboard views for displaying statistics and quick actions
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from apps.contacts.models import Contact
from apps.accounts.models import AdminUser


@login_required
def index(request):
    """
    Dashboard home page showing statistics and quick actions
    """
    # Get statistics
    total_contacts = Contact.objects.count()
    total_users = AdminUser.objects.filter(is_active=True).count()
    active_subscriptions = 0  # TODO: Implement when subscription model is ready
    
    context = {
        'total_contacts': total_contacts,
        'total_users': total_users,
        'active_subscriptions': active_subscriptions,
    }
    
    return render(request, 'dashboard/index.html', context)

