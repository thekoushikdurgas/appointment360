"""
Core models for task tracking and system-wide functionality
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TaskTracker(models.Model):
    """Track overall feature/task completion"""
    
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]
    
    CATEGORY_CHOICES = [
        ('SETUP', 'Setup'),
        ('IMPORT', 'Import'),
        ('EXPORT', 'Export'),
        ('ANALYTICS', 'Analytics'),
        ('UI_UX', 'UI/UX'),
        ('TESTING', 'Testing'),
        ('PERFORMANCE', 'Performance'),
        ('DOCUMENTATION', 'Documentation'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    task_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    order = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'order', 'task_name']
        verbose_name = 'Task Tracker'
        verbose_name_plural = 'Task Trackers'
    
    def __str__(self):
        return f"{self.get_category_display()}: {self.task_name}"
    
    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed and self.completed_at:
            self.completed_at = None
        super().save(*args, **kwargs)


class TaskCategory(models.Model):
    """Task categories for organization"""
    
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    icon = models.CharField(max_length=50, default='fas fa-tasks', help_text='Font Awesome icon class')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Task Category'
        verbose_name_plural = 'Task Categories'
    
    def __str__(self):
        return self.name
    
    @property
    def completion_percentage(self):
        """Calculate completion percentage for this category"""
        total_tasks = TaskTracker.objects.filter(category=self.name).count()
        if total_tasks == 0:
            return 0
        
        completed_tasks = TaskTracker.objects.filter(
            category=self.name, 
            is_completed=True
        ).count()
        
        return round((completed_tasks / total_tasks) * 100, 1)
    
    @property
    def completed_tasks_count(self):
        """Get count of completed tasks in this category"""
        return TaskTracker.objects.filter(
            category=self.name, 
            is_completed=True
        ).count()
    
    @property
    def total_tasks_count(self):
        """Get total count of tasks in this category"""
        return TaskTracker.objects.filter(category=self.name).count()


class SystemSettings(models.Model):
    """System-wide settings and configuration"""
    
    SETTING_TYPES = [
        ('BOOLEAN', 'Boolean'),
        ('STRING', 'String'),
        ('INTEGER', 'Integer'),
        ('JSON', 'JSON'),
    ]
    
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    setting_type = models.CharField(max_length=10, choices=SETTING_TYPES, default='STRING')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Settings'
    
    def __str__(self):
        return f"{self.key}: {self.value}"
    
    def get_value(self):
        """Get the value with proper type conversion"""
        if self.setting_type == 'BOOLEAN':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.setting_type == 'INTEGER':
            try:
                return int(self.value)
            except ValueError:
                return 0
        elif self.setting_type == 'JSON':
            import json
            try:
                return json.loads(self.value)
            except json.JSONDecodeError:
                return {}
        else:
            return self.value
    
    def set_value(self, value):
        """Set the value with proper type conversion"""
        if self.setting_type == 'BOOLEAN':
            self.value = str(bool(value)).lower()
        elif self.setting_type == 'INTEGER':
            self.value = str(int(value))
        elif self.setting_type == 'JSON':
            import json
            self.value = json.dumps(value)
        else:
            self.value = str(value)
