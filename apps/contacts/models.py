"""
Contact Model - Comprehensive contact management
Migrated from Stremlit/models/contact.py
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Contact(models.Model):
    """Contact model with all 40+ fields from Streamlit"""
    
    # Personal Information
    full_name = models.CharField(max_length=255, db_index=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    title = models.CharField(max_length=255, blank=True)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=50, blank=True)
    
    # Company Information
    company = models.CharField(max_length=255, db_index=True, blank=True)
    industry = models.CharField(max_length=150, db_index=True, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    company_address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    # Extended Company Fields
    employees_count = models.IntegerField(null=True, blank=True)
    annual_revenue = models.IntegerField(null=True, blank=True)
    total_funding = models.IntegerField(null=True, blank=True)
    latest_funding_amount = models.IntegerField(null=True, blank=True)
    
    # Additional Person Fields
    seniority = models.CharField(max_length=100, blank=True)
    departments = models.TextField(blank=True)  # Comma separated
    keywords = models.TextField(blank=True)
    technologies = models.TextField(blank=True)
    email_status = models.CharField(max_length=50, blank=True)
    stage = models.CharField(max_length=50, blank=True)  # Cold, Warm, Hot
    
    # Location
    city = models.CharField(max_length=150, db_index=True, blank=True)
    state = models.CharField(max_length=100, db_index=True, blank=True)
    country = models.CharField(max_length=100, db_index=True, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Company Location
    company_city = models.CharField(max_length=150, blank=True)
    company_state = models.CharField(max_length=100, blank=True)
    company_country = models.CharField(max_length=100, blank=True)
    company_phone = models.CharField(max_length=50, blank=True)
    
    # Social Media
    linkedin = models.URLField(blank=True)
    person_linkedin_url = models.URLField(blank=True)
    company_linkedin_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    facebook = models.CharField(max_length=255, blank=True)  # Keep for backward compatibility
    twitter_url = models.URLField(blank=True)
    twitter = models.CharField(max_length=255, blank=True)  # Keep for backward compatibility
    
    # Additional Fields
    notes = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default="active")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)  # Supabase UUID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contacts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['company'], name='company_idx'),
            models.Index(fields=['industry'], name='industry_idx'),
            models.Index(fields=['country'], name='country_idx'),
            models.Index(fields=['city'], name='city_idx'),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    def __repr__(self):
        return f"<Contact {self.full_name} ({self.email})>"

