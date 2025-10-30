"""
Analytics app URLs
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_dashboard, name='dashboard'),
    path('data-quality/', views.data_quality, name='data_quality'),
    
    # API endpoints for analytics
    path('api/chart-data/<str:chart_type>/', views.chart_data_api, name='chart_data_api'),
    path('api/stats/', views.analytics_stats_api, name='analytics_stats_api'),
]
