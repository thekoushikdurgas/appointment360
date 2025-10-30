"""
Core app views
"""
import json
import plotly.graph_objects as go
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from services.contact_service import ContactService
from .models import TaskTracker, TaskCategory


def loading_view(request):
    """Loading page view"""
    return render(request, 'core/loading.html')


def welcome_view(request):
    """Welcome page view"""
    # If user is authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    return render(request, 'core/welcome.html')


def dashboard(request):
    """Dashboard view with metrics and charts"""
    # Get contact statistics
    stats = ContactService.get_contact_stats()
    
    # Create metric cards data
    metrics = [
        {
            'label': 'Total Contacts',
            'value': stats['total'],
            'icon': '<i class="fas fa-address-card"></i>',
            'color_from': '#FF6B35',
            'color_to': '#FF8C42'
        },
        {
            'label': 'Industries',
            'value': stats['industries'],
            'icon': '<i class="fas fa-industry"></i>',
            'color_from': '#4CAF50',
            'color_to': '#81C784'
        },
        {
            'label': 'Countries',
            'value': stats['countries'],
            'icon': '<i class="fas fa-globe"></i>',
            'color_from': '#2196F3',
            'color_to': '#64B5F6'
        },
        {
            'label': 'Active Contacts',
            'value': stats['active'],
            'icon': '<i class="fas fa-check-circle"></i>',
            'color_from': '#9C27B0',
            'color_to': '#BA68C8'
        }
    ]
    
    # Get chart data
    industry_data = ContactService.get_industry_distribution(limit=10)
    country_data = ContactService.get_country_distribution(limit=10)
    
    # Create industry distribution chart
    industry_chart = None
    if industry_data:
        industries = [item['industry'] for item in industry_data]
        counts = [item['count'] for item in industry_data]
        
        fig = go.Figure(data=go.Bar(
            x=counts,
            y=industries,
            orientation='h',
            marker=dict(color='#FF6B35'),
            hovertemplate='%{y}: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10),
            height=300
        )
        
        industry_chart = fig.to_html(
            div_id='industry-chart',
            include_plotlyjs=False,
            config={'displayModeBar': False}
        )
    
    # Create country distribution chart
    country_chart = None
    if country_data:
        countries = [item['country'] for item in country_data]
        counts = [item['count'] for item in country_data]
        
        fig = go.Figure(data=go.Bar(
            x=counts,
            y=countries,
            orientation='h',
            marker=dict(color='#4CAF50'),
            hovertemplate='%{y}: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10),
            height=300
        )
        
        country_chart = fig.to_html(
            div_id='country-chart',
            include_plotlyjs=False,
            config={'displayModeBar': False}
        )
    
    context = {
        'page_title': 'Dashboard',
        'metrics': metrics,
        'industry_chart': industry_chart,
        'country_chart': country_chart
    }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def progress_tracker_view(request):
    """Display overall task tracker page"""
    categories = TaskCategory.objects.filter(is_active=True).order_by('order')
    tasks = TaskTracker.objects.all().order_by('category', 'order')
    
    context = {
        'page_title': 'Progress Tracker',
        'categories': categories,
        'tasks': tasks
    }
    
    return render(request, 'core/progress_tracker.html', context)


@login_required
def categories_api(request):
    """Get task categories as JSON"""
    try:
        categories = TaskCategory.objects.filter(is_active=True).order_by('order')
        
        categories_data = []
        for category in categories:
            categories_data.append({
                'name': category.name,
                'description': category.description,
                'color': category.color,
                'icon': category.icon,
                'order': category.order,
                'completion_percentage': category.completion_percentage,
                'completed_tasks_count': category.completed_tasks_count,
                'total_tasks_count': category.total_tasks_count
            })
        
        return JsonResponse({
            'categories': categories_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def tasks_api(request):
    """Get tasks as JSON"""
    try:
        tasks = TaskTracker.objects.all().order_by('category', 'order')
        
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                'category': task.category,
                'task_name': task.task_name,
                'description': task.description,
                'is_completed': task.is_completed,
                'priority': task.priority,
                'order': task.order,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat()
            })
        
        return JsonResponse({
            'tasks': tasks_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def update_task_status_api(request, task_id):
    """Toggle task completion status"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        task = TaskTracker.objects.get(id=task_id)
        
        data = json.loads(request.body)
        is_completed = data.get('is_completed', not task.is_completed)
        
        task.is_completed = is_completed
        if is_completed and not task.completed_at:
            task.completed_at = timezone.now()
        elif not is_completed:
            task.completed_at = None
        
        task.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Task "{task.task_name}" {"completed" if is_completed else "reopened"}',
            'task': {
                'id': task.id,
                'task_name': task.task_name,
                'is_completed': task.is_completed,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None
            }
        })
        
    except TaskTracker.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def progress_stats_api(request):
    """Get overall progress statistics"""
    try:
        total_tasks = TaskTracker.objects.count()
        completed_tasks = TaskTracker.objects.filter(is_completed=True).count()
        remaining_tasks = total_tasks - completed_tasks
        
        overall_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Category breakdown
        categories_data = []
        for category_code, category_name in TaskTracker.CATEGORY_CHOICES:
            category_tasks = TaskTracker.objects.filter(category=category_code)
            category_completed = category_tasks.filter(is_completed=True).count()
            category_total = category_tasks.count()
            category_progress = (category_completed / category_total * 100) if category_total > 0 else 0
            
            categories_data.append({
                'code': category_code,
                'name': category_name,
                'total_tasks': category_total,
                'completed_tasks': category_completed,
                'progress_percentage': round(category_progress, 1)
            })
        
        return JsonResponse({
            'overall_progress': round(overall_progress, 1),
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'remaining_tasks': remaining_tasks,
            'categories': categories_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
