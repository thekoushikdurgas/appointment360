"""
Core app URLs
"""
from django.urls import path
from . import views
from . import sse_views

app_name = 'core'

urlpatterns = [
    path('loading/', views.loading_view, name='loading'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('progress-tracker/', views.progress_tracker_view, name='progress_tracker'),
    
    # API endpoints for progress tracker
    path('api/categories/', views.categories_api, name='categories_api'),
    path('api/tasks/', views.tasks_api, name='tasks_api'),
    path('api/tasks/<int:task_id>/toggle/', views.update_task_status_api, name='update_task_status_api'),
    path('api/progress-stats/', views.progress_stats_api, name='progress_stats_api'),
    
    # Server-Sent Events endpoints
    path('sse/updates/', sse_views.sse_updates, name='sse_updates'),
    path('sse/send-notification/', sse_views.send_notification, name='send_notification'),
    path('sse/status/', sse_views.sse_status, name='sse_status'),
]

