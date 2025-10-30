"""
Job Scraper URL Configuration
"""
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_scraper_view, name='scraper'),
    path('results/', views.job_results_view, name='results'),
    path('api/scrape/', views.job_scraper_api, name='api_scrape'),
    path('api/status/', views.job_scraper_status, name='api_status'),
    path('test/', views.test_scraper, name='test'),
]
