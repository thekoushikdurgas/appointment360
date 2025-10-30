from django.contrib import admin
from .models import ImportJob


@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'status', 'total_rows', 'processed_rows', 'success_count', 'error_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['filename', 'user_id']
    readonly_fields = ['created_at', 'started_at', 'completed_at']
    
    fieldsets = (
        ('Job Information', {
            'fields': ('filename', 'file_size', 'user_id', 'status')
        }),
        ('Progress', {
            'fields': ('total_rows', 'processed_rows', 'success_count', 'error_count', 'duplicate_count')
        }),
        ('Performance', {
            'fields': ('processing_speed', 'current_batch', 'total_batches', 'estimated_completion')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'completed_at', 'created_at')
        }),
        ('Metadata', {
            'fields': ('error_log', 'column_mapping'),
            'classes': ('collapse',)
        }),
    )

