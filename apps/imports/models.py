"""
Import Job Model - Track background import jobs
Migrated from Stremlit/models/import_job.py
"""
from django.db import models
from django.core.validators import MinValueValidator


class ImportJob(models.Model):
    """Import job model for tracking background import jobs"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Job Information
    user_id = models.CharField(max_length=255, null=True, blank=True)  # Supabase UUID
    filename = models.CharField(max_length=500)
    file_size = models.BigIntegerField(null=True, blank=True)  # File size in bytes
    
    # Progress Tracking
    total_rows = models.IntegerField(default=0)
    processed_rows = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    duplicate_count = models.IntegerField(default=0)
    
    # Status
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING',
        db_index=True
    )
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    error_log = models.TextField(blank=True)  # JSON string of errors
    column_mapping = models.TextField(blank=True)  # JSON string of column mappings
    
    # Performance Metrics
    processing_speed = models.FloatField(null=True, blank=True)  # rows per second
    estimated_completion = models.DateTimeField(null=True, blank=True)
    
    # Batch Information
    current_batch = models.IntegerField(default=0)
    total_batches = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'import_jobs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"ImportJob {self.id}: {self.filename} ({self.status})"
    
    def get_progress_percentage(self):
        """Calculate progress percentage"""
        if self.total_rows == 0:
            return 0.0
        return (self.processed_rows / self.total_rows) * 100
    
    def is_complete(self):
        """Check if job is complete"""
        return self.status in ['COMPLETED', 'FAILED', 'CANCELLED']
    
    def is_running(self):
        """Check if job is currently running"""
        return self.status == 'PROCESSING'
    
    def get_remaining_rows(self):
        """Get number of rows remaining"""
        return max(0, self.total_rows - self.processed_rows)

