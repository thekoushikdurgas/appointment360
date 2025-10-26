from django.db import models
from apps.core.models import TimeStampedModel


class Industry(TimeStampedModel):
    """Industry model for categorizing contacts"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'industries'
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Contact(TimeStampedModel):
    """
    Contact model with 48+ fields matching Laravel schema
    Stores contact information for companies and individuals
    """
    
    # Personal Information
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    seniority = models.CharField(max_length=100, blank=True, null=True)
    departments = models.CharField(max_length=255, blank=True, null=True)
    
    # Contact Information
    email = models.EmailField(db_index=True, blank=True, null=True)
    email_status = models.CharField(max_length=50, blank=True, null=True)
    primary_email_catch_all_status = models.CharField(max_length=50, blank=True, null=True)
    
    # Phone Numbers
    work_direct_phone = models.CharField(max_length=50, blank=True, null=True)
    home_phone = models.CharField(max_length=50, blank=True, null=True)
    mobile_phone = models.CharField(max_length=50, blank=True, null=True)
    corporate_phone = models.CharField(max_length=50, blank=True, null=True)
    other_phone = models.CharField(max_length=50, blank=True, null=True)
    
    # Company Information
    company = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    company_name_for_emails = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    industry_model = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contacts'
    )
    employees = models.IntegerField(null=True, blank=True)
    stage = models.CharField(max_length=100, blank=True, null=True)
    
    # Financial Information
    annual_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    total_funding = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    latest_funding = models.CharField(max_length=50, blank=True, null=True)
    latest_funding_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    last_raised_at = models.DateField(blank=True, null=True)
    
    # Location Information
    city = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    state = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    country = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    
    # Company Location
    company_address = models.TextField(blank=True, null=True)
    company_city = models.CharField(max_length=100, blank=True, null=True)
    company_state = models.CharField(max_length=100, blank=True, null=True)
    company_country = models.CharField(max_length=100, blank=True, null=True)
    company_phone = models.CharField(max_length=50, blank=True, null=True)
    
    # Technologies and Keywords
    technologies = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    
    # Social Media & URLs
    person_linkedin_url = models.URLField(blank=True, null=True)
    company_linkedin_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # External IDs
    contact_id = models.CharField(max_length=100, blank=True, null=True)
    account_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'contacts'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['company', 'industry']),
            models.Index(fields=['city', 'country']),
            models.Index(fields=['email_status']),
            models.Index(fields=['employees']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company or 'No Company'}"
    
    @property
    def full_name(self):
        """Return full name of contact"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def location(self):
        """Return location string"""
        parts = [self.city, self.state, self.country]
        return ', '.join(filter(None, parts))

