"""
Imports app URLs
"""
from django.urls import path
from . import views

app_name = 'imports'

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('start/', views.start_import_view, name='start'),
    path('progress/<int:job_id>/', views.progress_view, name='progress'),
    
    # API endpoints for progress tracking
    path('api/job/<int:job_id>/status/', views.job_status_api, name='job_status_api'),
    path('api/job/<int:job_id>/cancel/', views.cancel_job_api, name='cancel_job_api'),
    path('api/recent-jobs/', views.recent_jobs_api, name='recent_jobs_api'),
]

