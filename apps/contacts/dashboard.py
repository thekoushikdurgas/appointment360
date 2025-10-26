"""
Dashboard views and statistics
"""
from django.db.models import Count, Avg, Sum, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Contact, Industry


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics
    """
    # Total contacts count
    total_contacts = Contact.objects.count()
    
    # Contacts by status
    verified_emails = Contact.objects.filter(email_status='Verified').count()
    unverified_emails = Contact.objects.filter(email_status__in=['Unverified', 'Invalid']).count()
    
    # Contacts by industry (top 5)
    top_industries = Contact.objects.values('industry').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Geographic distribution (top 5 countries)
    top_countries = Contact.objects.values('country').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Average employees per company
    avg_employees = Contact.objects.filter(employees__isnull=False).aggregate(
        avg=Avg('employees')
    )['avg'] or 0
    
    # Total companies
    total_companies = Contact.objects.values('company').distinct().count()
    
    # Revenue statistics
    avg_revenue = Contact.objects.filter(annual_revenue__isnull=False).aggregate(
        avg=Avg('annual_revenue')
    )['avg'] or 0
    
    total_revenue = Contact.objects.filter(annual_revenue__isnull=False).aggregate(
        total=Sum('annual_revenue')
    )['total'] or 0
    
    # Contacts with LinkedIn
    with_linkedin = Contact.objects.exclude(
        Q(person_linkedin_url__isnull=True) | Q(person_linkedin_url='')
    ).count()
    
    # Recent contacts (last 7 days)
    from django.utils import timezone
    from datetime import timedelta
    recent_contacts = Contact.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    return Response({
        'success': True,
        'stats': {
            'total_contacts': total_contacts,
            'verified_emails': verified_emails,
            'unverified_emails': unverified_emails,
            'top_industries': list(top_industries),
            'top_countries': list(top_countries),
            'avg_employees': round(avg_employees, 2),
            'total_companies': total_companies,
            'avg_revenue': float(avg_revenue),
            'total_revenue': float(total_revenue),
            'with_linkedin': with_linkedin,
            'recent_contacts': recent_contacts
        }
    })

