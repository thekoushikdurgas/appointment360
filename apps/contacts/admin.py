"""
Admin configuration for Contact models
"""
from django.contrib import admin
from .models import Contact, Industry


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    """Admin interface for Industry model"""
    list_display = ('name', 'description', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin interface for Contact model"""
    
    list_display = (
        'full_name',
        'title',
        'email',
        'company',
        'city',
        'country',
        'industry',
        'employees',
        'email_status',
        'created_at'
    )
    
    list_filter = (
        'email_status',
        'industry',
        'country',
        'state',
        'created_at',
        'updated_at'
    )
    
    search_fields = (
        'first_name',
        'last_name',
        'email',
        'company',
        'title',
        'city',
        'country'
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'title', 'seniority', 'departments')
        }),
        ('Contact Information', {
            'fields': (
                'email', 'email_status', 'primary_email_catch_all_status',
                'work_direct_phone', 'home_phone', 'mobile_phone', 'corporate_phone', 'other_phone'
            )
        }),
        ('Company Information', {
            'fields': (
                'company', 'company_name_for_emails', 'industry', 'industry_model',
                'employees', 'stage'
            )
        }),
        ('Financial Information', {
            'fields': (
                'annual_revenue', 'total_funding', 'latest_funding',
                'latest_funding_amount', 'last_raised_at'
            )
        }),
        ('Location Information', {
            'fields': (
                'city', 'state', 'country',
                'company_address', 'company_city', 'company_state', 'company_country', 'company_phone'
            )
        }),
        ('Social & Web', {
            'fields': (
                'person_linkedin_url', 'company_linkedin_url',
                'facebook_url', 'twitter_url', 'website'
            )
        }),
        ('Metadata', {
            'fields': ('technologies', 'keywords', 'contact_id', 'account_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
    
    ordering = ('-created_at',)
    
    # Customize display for large datasets
    list_per_page = 50
    list_max_show_all = 500

