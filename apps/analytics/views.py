"""
Analytics views
"""
import plotly.graph_objects as go
import plotly.express as px
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from apps.contacts.models import Contact
from apps.imports.models import ImportJob
from apps.exports.models import ExportLog


@login_required
def analytics_dashboard(request):
    """Enhanced analytics dashboard view with comprehensive charts"""
    
    # Get date range from request (default to last 30 days)
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Get basic statistics
    total_contacts = Contact.objects.count()
    active_contacts = Contact.objects.filter(is_active=True).count()
    
    # Get industry distribution
    industry_data = Contact.objects.filter(
        industry__isnull=False
    ).exclude(industry='').values('industry').annotate(
        count=Count('id')
    ).order_by('-count')[:15]
    
    # Get country distribution
    country_data = Contact.objects.filter(
        country__isnull=False
    ).exclude(country='').values('country').annotate(
        count=Count('id')
    ).order_by('-count')[:15]
    
    # Get contact growth trend
    growth_data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        count = Contact.objects.filter(created_at__date=date.date()).count()
        growth_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Get top companies by employee count (if we have that data)
    top_companies = Contact.objects.filter(
        company__isnull=False
    ).exclude(company='').values('company').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Get contact status distribution
    status_data = Contact.objects.values('is_active').annotate(
        count=Count('id')
    )
    
    # Get import/export statistics
    total_imports = ImportJob.objects.count()
    successful_imports = ImportJob.objects.filter(status='COMPLETED').count()
    total_exports = ExportLog.objects.count()
    
    # Create charts
    charts = {}
    
    # Industry Distribution Chart
    if industry_data:
        industries = [item['industry'] for item in industry_data]
        counts = [item['count'] for item in industry_data]
        
        fig = go.Figure(data=go.Bar(
            x=counts,
            y=industries,
            orientation='h',
            marker=dict(
                color=px.colors.qualitative.Set3[:len(industries)],
                line=dict(color='rgba(0,0,0,0.1)', width=1)
            ),
            hovertemplate='<b>%{y}</b><br>Contacts: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Industry Distribution',
            xaxis_title='Number of Contacts',
            yaxis_title='Industry',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
            height=400
        )
        
        charts['industry'] = fig.to_html(
            div_id='industry-chart',
            include_plotlyjs=False,
            config={'displayModeBar': True, 'displaylogo': False}
        )
    
    # Country Distribution Chart
    if country_data:
        countries = [item['country'] for item in country_data]
        counts = [item['count'] for item in country_data]
        
        fig = go.Figure(data=go.Bar(
            x=counts,
            y=countries,
            orientation='h',
            marker=dict(
                color=px.colors.qualitative.Pastel[:len(countries)],
                line=dict(color='rgba(0,0,0,0.1)', width=1)
            ),
            hovertemplate='<b>%{y}</b><br>Contacts: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Country Distribution',
            xaxis_title='Number of Contacts',
            yaxis_title='Country',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
            height=400
        )
        
        charts['country'] = fig.to_html(
            div_id='country-chart',
            include_plotlyjs=False,
            config={'displayModeBar': True, 'displaylogo': False}
        )
    
    # Contact Growth Trend Chart
    if growth_data:
        dates = [item['date'] for item in growth_data]
        counts = [item['count'] for item in growth_data]
        
        fig = go.Figure(data=go.Scatter(
            x=dates,
            y=counts,
            mode='lines+markers',
            line=dict(color='#FF6B35', width=3),
            marker=dict(size=6, color='#FF6B35'),
            hovertemplate='<b>%{x}</b><br>New Contacts: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Contact Growth Trend ({days} days)',
            xaxis_title='Date',
            yaxis_title='New Contacts',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
            height=300
        )
        
        charts['growth'] = fig.to_html(
            div_id='growth-chart',
            include_plotlyjs=False,
            config={'displayModeBar': True, 'displaylogo': False}
        )
    
    # Top Companies Chart
    if top_companies:
        companies = [item['company'] for item in top_companies]
        counts = [item['count'] for item in top_companies]
        
        fig = go.Figure(data=go.Bar(
            x=companies,
            y=counts,
            marker=dict(
                color=px.colors.qualitative.Vivid[:len(companies)],
                line=dict(color='rgba(0,0,0,0.1)', width=1)
            ),
            hovertemplate='<b>%{x}</b><br>Contacts: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Top Companies by Contact Count',
            xaxis_title='Company',
            yaxis_title='Number of Contacts',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
            height=300,
            xaxis_tickangle=-45
        )
        
        charts['companies'] = fig.to_html(
            div_id='companies-chart',
            include_plotlyjs=False,
            config={'displayModeBar': True, 'displaylogo': False}
        )
    
    # Contact Status Pie Chart
    if status_data:
        labels = ['Active', 'Inactive']
        values = [0, 0]
        
        for item in status_data:
            if item['is_active']:
                values[0] = item['count']
            else:
                values[1] = item['count']
        
        fig = go.Figure(data=go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=['#4CAF50', '#FF9800']),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Contact Status Distribution',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            margin=dict(l=10, r=10, t=40, b=10),
            height=300
        )
        
        charts['status'] = fig.to_html(
            div_id='status-chart',
            include_plotlyjs=False,
            config={'displayModeBar': True, 'displaylogo': False}
        )
    
    context = {
        'page_title': 'Analytics Dashboard',
        'total_contacts': total_contacts,
        'active_contacts': active_contacts,
        'total_imports': total_imports,
        'successful_imports': successful_imports,
        'total_exports': total_exports,
        'charts': charts,
        'days': days,
        'industry_data': list(industry_data),
        'country_data': list(country_data),
        'growth_data': growth_data,
        'top_companies': list(top_companies),
        'status_data': list(status_data)
    }
    
    return render(request, 'analytics/dashboard.html', context)


@login_required
def data_quality(request):
    """Data quality analysis view"""
    
    # Calculate quality metrics
    total = Contact.objects.count()
    
    # Email completeness
    with_email = Contact.objects.filter(email__isnull=False).exclude(email='').count()
    email_pct = (with_email / total * 100) if total > 0 else 0
    
    # Phone completeness
    with_phone = Contact.objects.filter(phone__isnull=False).exclude(phone='').count()
    phone_pct = (with_phone / total * 100) if total > 0 else 0
    
    # Company completeness
    with_company = Contact.objects.filter(company__isnull=False).exclude(company='').count()
    company_pct = (with_company / total * 100) if total > 0 else 0
    
    # Overall quality score
    quality_score = (email_pct * 0.4 + phone_pct * 0.3 + company_pct * 0.3)
    
    # Get duplicates
    duplicates = Contact.objects.values('email').annotate(
        count=Count('email')
    ).filter(count__gt=1).count()
    
    # Missing data
    missing_emails = total - with_email
    missing_phones = total - with_phone
    missing_companies = total - with_company
    
    context = {
        'page_title': 'Data Quality',
        'total': total,
        'email_pct': email_pct,
        'phone_pct': phone_pct,
        'company_pct': company_pct,
        'quality_score': quality_score,
        'duplicates': duplicates,
        'missing_emails': missing_emails,
        'missing_phones': missing_phones,
        'missing_companies': missing_companies,
    }
    
    return render(request, 'analytics/data_quality.html', context)


@login_required
def chart_data_api(request, chart_type):
    """Return chart data as JSON for dynamic updates"""
    try:
        days = int(request.GET.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        if chart_type == 'industry':
            data = Contact.objects.filter(
                industry__isnull=False
            ).exclude(industry='').values('industry').annotate(
                count=Count('id')
            ).order_by('-count')[:15]
            
            return JsonResponse({
                'labels': [item['industry'] for item in data],
                'values': [item['count'] for item in data],
                'chart_type': 'bar_horizontal'
            })
            
        elif chart_type == 'country':
            data = Contact.objects.filter(
                country__isnull=False
            ).exclude(country='').values('country').annotate(
                count=Count('id')
            ).order_by('-count')[:15]
            
            return JsonResponse({
                'labels': [item['country'] for item in data],
                'values': [item['count'] for item in data],
                'chart_type': 'bar_horizontal'
            })
            
        elif chart_type == 'growth':
            growth_data = []
            for i in range(days):
                date = start_date + timedelta(days=i)
                count = Contact.objects.filter(created_at__date=date.date()).count()
                growth_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'count': count
                })
            
            return JsonResponse({
                'dates': [item['date'] for item in growth_data],
                'values': [item['count'] for item in growth_data],
                'chart_type': 'line'
            })
            
        elif chart_type == 'companies':
            data = Contact.objects.filter(
                company__isnull=False
            ).exclude(company='').values('company').annotate(
                count=Count('id')
            ).order_by('-count')[:10]
            
            return JsonResponse({
                'labels': [item['company'] for item in data],
                'values': [item['count'] for item in data],
                'chart_type': 'bar'
            })
            
        elif chart_type == 'status':
            data = Contact.objects.values('is_active').annotate(
                count=Count('id')
            )
            
            labels = ['Active', 'Inactive']
            values = [0, 0]
            
            for item in data:
                if item['is_active']:
                    values[0] = item['count']
                else:
                    values[1] = item['count']
            
            return JsonResponse({
                'labels': labels,
                'values': values,
                'chart_type': 'pie'
            })
            
        else:
            return JsonResponse({'error': 'Invalid chart type'}, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def analytics_stats_api(request):
    """Get analytics statistics as JSON"""
    try:
        # Get basic statistics
        total_contacts = Contact.objects.count()
        active_contacts = Contact.objects.filter(is_active=True).count()
        
        # Get import/export statistics
        total_imports = ImportJob.objects.count()
        successful_imports = ImportJob.objects.filter(status='COMPLETED').count()
        total_exports = ExportLog.objects.count()
        
        # Get recent activity (last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        recent_contacts = Contact.objects.filter(created_at__gte=week_ago).count()
        recent_imports = ImportJob.objects.filter(created_at__gte=week_ago).count()
        recent_exports = ExportLog.objects.filter(created_at__gte=week_ago).count()
        
        return JsonResponse({
            'total_contacts': total_contacts,
            'active_contacts': active_contacts,
            'total_imports': total_imports,
            'successful_imports': successful_imports,
            'total_exports': total_exports,
            'recent_contacts': recent_contacts,
            'recent_imports': recent_imports,
            'recent_exports': recent_exports,
            'import_success_rate': round((successful_imports / total_imports * 100), 1) if total_imports > 0 else 0
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

