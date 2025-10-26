from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import AdminUser


@admin.register(AdminUser)
class AdminUserAdmin(BaseUserAdmin):
    """Custom admin interface for AdminUser model"""
    
    list_display = (
        'username',
        'email',
        'name',
        'role',
        'is_active',
        'download_limit',
        'last_login',
        'date_joined'
    )
    
    list_filter = (
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined'
    )
    
    search_fields = (
        'username',
        'email',
        'name',
        'first_name',
        'last_name'
    )
    
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'role',
                'column_allowed',
                'groups',
                'user_permissions'
            ),
        }),
        ('Account Settings', {
            'fields': ('download_limit', 'created_by', 'reset_token'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'role', 'password1', 'password2'),
        }),
    )

