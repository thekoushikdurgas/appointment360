"""
Models for Parcel Type management
"""
from django.db import models
from apps.core.models import TimeStampedModel


class ParcelType(TimeStampedModel):
    """
    Parcel Type model for delivery types
    """
    STATUS_CHOICES = [
        ('y', 'Active'),
        ('n', 'Inactive'),
    ]
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n')
    
    class Meta:
        db_table = 'parcel_types'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_image_url(self):
        """Get full image URL"""
        if self.image:
            return f'/media/files/parcel_types/{self.image}'
        return None
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
