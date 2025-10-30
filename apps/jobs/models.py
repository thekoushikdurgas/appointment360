"""
Job Scraper Models
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ScrapingJob(models.Model):
    """
    Model to track scraping jobs.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_jobs = models.IntegerField(default=0)
    processed_jobs = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Scraping Job {self.id} - {self.url}"


class ScrapedJob(models.Model):
    """
    Model to store scraped job data.
    """
    scraping_job = models.ForeignKey(ScrapingJob, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=500, blank=True)
    raw_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
