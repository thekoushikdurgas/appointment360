"""
User Model with Supabase Integration
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model integrated with Supabase"""
    
    # Supabase fields
    supabase_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    supabase_email = models.EmailField(unique=True, null=True, blank=True)
    
    # Additional fields
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    # Profile picture stored as URL in Supabase Storage
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    
    # Verification status
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    # Timestamps
    is_active = models.BooleanField(default=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email or self.username
    
    def get_profile_picture_url(self):
        """Get profile picture URL or default avatar"""
        if self.profile_picture:
            return self.profile_picture
        # Return default avatar URL
        return f"https://ui-avatars.com/api/?name={self.get_full_name()}&background=FF6B35&color=fff"
    
    def get_full_name(self):
        """Get full name or username"""
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username

