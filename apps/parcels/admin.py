"""
Admin interface for parcel types
"""
from django.contrib import admin
from .models import ParcelType


@admin.register(ParcelType)
class ParcelTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
