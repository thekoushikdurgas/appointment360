"""
Exports app URLs
"""
from django.urls import path
from . import views

app_name = 'exports'

urlpatterns = [
    path('history/', views.export_history, name='history'),
    
    # API endpoints
    path('api/status/<int:export_id>/', views.export_status_api, name='export_status_api'),
    path('api/download/<int:export_id>/', views.download_export, name='download_export'),
    path('api/cancel/<int:export_id>/', views.cancel_export_api, name='cancel_export_api'),
    path('api/delete/<int:export_id>/', views.delete_export_api, name='delete_export_api'),
    path('api/bulk-delete/', views.bulk_delete_exports_api, name='bulk_delete_exports_api'),
    path('api/stats/', views.export_stats_api, name='export_stats_api'),
    path('api/create/', views.create_export_api, name='create_export_api'),
]

