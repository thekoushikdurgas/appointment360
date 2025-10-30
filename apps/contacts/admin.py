from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'company', 'industry', 'country', 'is_active', 'created_at']
    list_filter = ['industry', 'country', 'is_active', 'created_at']
    search_fields = ['full_name', 'email', 'company', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'first_name', 'last_name', 'title', 'email', 'phone')
        }),
        ('Company Information', {
            'fields': ('company', 'industry', 'company_size', 'website')
        }),
        ('Location', {
            'fields': ('city', 'state', 'country', 'postal_code')
        }),
        ('Additional', {
            'fields': ('linkedin', 'notes', 'tags', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

