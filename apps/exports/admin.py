from django.contrib import admin
from .models import ExportLog, ExportLimit


@admin.register(ExportLog)
class ExportLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'export_type', 'export_format', 'record_count', 'created_at']
    list_filter = ['export_type', 'export_format', 'created_at']
    search_fields = ['user_id', 'filename']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(ExportLimit)
class ExportLimitAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'date', 'export_count', 'limit', 'last_export_at']
    list_filter = ['date']
    search_fields = ['user_id']

