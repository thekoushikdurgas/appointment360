from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class AdminUser(AbstractUser):
    """
    Extended User model for admin functionality
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('user', 'Regular User'),
        ('manager', 'Manager'),
    ]
    
    name = models.CharField(max_length=255, help_text="Full name of the user")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users',
        help_text="User who created this account"
    )
    download_limit = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0)],
        help_text="Maximum number of downloads allowed"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user account is active"
    )
    column_allowed = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        help_text="JSON field storing column permission settings"
    )
    reset_token = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Token for password reset"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Last known IP address"
    )
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address used in last login"
    )
    
    class Meta:
        db_table = 'admin_users'
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    @property
    def can_export(self):
        """Check if user can export contacts"""
        return self.download_limit > 0 if hasattr(self, 'download_limit') else True
    
    def decrement_download_limit(self):
        """Decrement download limit by 1"""
        if self.download_limit > 0:
            self.download_limit -= 1
            self.save(update_fields=['download_limit'])

