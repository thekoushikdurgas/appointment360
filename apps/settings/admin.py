"""
Settings admin configuration
"""
from django.contrib import admin
from .models import UserSettings, FeatureToggle, UserFeatureToggle, SystemSettings


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'language', 'dashboard_layout', 'items_per_page']
    list_filter = ['theme', 'language', 'dashboard_layout', 'email_notifications']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('UI Preferences', {
            'fields': ('theme', 'language', 'timezone', 'dashboard_layout', 'items_per_page')
        }),
        ('Notifications', {
            'fields': ('email_notifications', 'push_notifications', 'import_completion_notifications', 
                      'export_completion_notifications', 'error_notifications')
        }),
        ('Feature Toggles', {
            'fields': ('enable_analytics', 'enable_bulk_operations', 'enable_progress_tracking', 
                      'enable_export_history', 'enable_data_quality_reports')
        }),
        ('Import/Export', {
            'fields': ('default_import_format', 'default_export_format', 'auto_delete_temp_files', 
                      'temp_file_retention_days')
        }),
        ('Security', {
            'fields': ('two_factor_enabled', 'session_timeout_minutes')
        }),
        ('Privacy', {
            'fields': ('data_retention_days', 'allow_data_sharing', 'allow_analytics_tracking')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FeatureToggle)
class FeatureToggleAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_enabled', 'is_global', 'rollout_percentage']
    list_filter = ['category', 'is_enabled', 'is_global']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Toggle Settings', {
            'fields': ('is_enabled', 'is_global')
        }),
        ('Rollout Settings', {
            'fields': ('rollout_percentage', 'target_user_groups')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserFeatureToggle)
class UserFeatureToggleAdmin(admin.ModelAdmin):
    list_display = ['user', 'feature', 'is_enabled']
    list_filter = ['is_enabled', 'feature__category']
    search_fields = ['user__username', 'feature__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'category', 'data_type', 'value']
    list_filter = ['category', 'data_type']
    search_fields = ['key', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('key', 'value', 'description', 'category', 'data_type')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
