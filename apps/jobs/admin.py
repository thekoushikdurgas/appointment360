"""
Job Scraper Admin Configuration
"""
from django.contrib import admin
from .models import ScrapingJob, ScrapedJob


@admin.register(ScrapingJob)
class ScrapingJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'url', 'status', 'total_jobs', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['url', 'user__email']
    readonly_fields = ['created_at', 'started_at', 'completed_at']


@admin.register(ScrapedJob)
class ScrapedJobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'scraping_job', 'created_at']
    list_filter = ['created_at', 'scraping_job__status']
    search_fields = ['title', 'company', 'location']
    readonly_fields = ['created_at']
