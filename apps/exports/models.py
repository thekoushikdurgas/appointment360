"""
Export Log Model - Track export history and limits
Migrated from Stremlit/models/export_log.py
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class ExportLog(models.Model):
    """Export log model for tracking export history"""
    
    EXPORT_TYPE_CHOICES = [
        ('contacts', 'Contacts'),
        ('analytics', 'Analytics'),
        ('quality_report', 'Quality Report'),
        ('bulk_export', 'Bulk Export'),
        ('selected_contacts', 'Selected Contacts'),
    ]
    
    EXPORT_FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('json', 'JSON'),
        ('pdf', 'PDF'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Export Information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    supabase_user_id = models.CharField(max_length=255, null=True, blank=True)  # Supabase UUID (legacy)
    export_type = models.CharField(max_length=50, choices=EXPORT_TYPE_CHOICES)
    export_format = models.CharField(max_length=20, choices=EXPORT_FORMAT_CHOICES, default='csv')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Statistics
    record_count = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    file_size = models.BigIntegerField(null=True, blank=True)  # File size in bytes
    
    # Additional Metadata
    filters_applied = models.JSONField(default=dict, blank=True)  # Store filter criteria
    filename = models.CharField(max_length=500, blank=True)
    file_path = models.CharField(max_length=1000, blank=True)  # Path to exported file
    
    # Progress tracking
    progress_percentage = models.FloatField(default=0.0)
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'export_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['supabase_user_id', 'created_at'], name='user_export_idx'),
            models.Index(fields=['export_type'], name='export_type_idx'),
        ]
    
    def __str__(self):
        return f"Export {self.id}: {self.export_type} ({self.export_format}) - {self.record_count} records"
    
    @property
    def duration(self):
        """Calculate export duration"""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None
    
    @property
    def is_completed(self):
        """Check if export is completed"""
        return self.status == 'completed'
    
    @property
    def is_failed(self):
        """Check if export failed"""
        return self.status == 'failed'
    
    @property
    def is_processing(self):
        """Check if export is processing"""
        return self.status == 'processing'
    
    @property
    def file_size_display(self):
        """Get human readable file size"""
        if not self.file_size:
            return 'Unknown'
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    def mark_as_started(self):
        """Mark export as started"""
        from django.utils import timezone
        self.status = 'processing'
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])
    
    def mark_as_completed(self, file_path=None, file_size=None):
        """Mark export as completed"""
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        if file_path:
            self.file_path = file_path
        if file_size:
            self.file_size = file_size
        self.progress_percentage = 100.0
        self.save(update_fields=['status', 'completed_at', 'file_path', 'file_size', 'progress_percentage'])
    
    def mark_as_failed(self, error_message=None):
        """Mark export as failed"""
        from django.utils import timezone
        self.status = 'failed'
        self.completed_at = timezone.now()
        if error_message:
            self.error_message = error_message
        self.save(update_fields=['status', 'completed_at', 'error_message'])


class ExportLimit(models.Model):
    """Export limit model for enforcing daily export limits"""
    
    user_id = models.CharField(max_length=255, unique=True, db_index=True)
    
    # Daily limit tracking
    date = models.DateField(auto_now_add=True)
    export_count = models.IntegerField(default=0)
    limit = models.IntegerField(default=100)  # Default limit
    
    # Timestamps
    reset_at = models.DateTimeField(auto_now_add=True)
    last_export_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'export_limits'
        ordering = ['-date']
    
    def __str__(self):
        return f"ExportLimit for user {self.user_id}: {self.export_count}/{self.limit}"
    
    def can_export(self):
        """Check if user can export"""
        return self.export_count < self.limit
    
    def get_remaining_exports(self):
        """Get remaining export count"""
        return max(0, self.limit - self.export_count)

