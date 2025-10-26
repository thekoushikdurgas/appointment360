"""
URL configuration for parcels app
"""
from django.urls import path
from .views import (
    parcel_type_list_view, parcel_type_create_view, parcel_type_delete_view
)

app_name = 'parcels'

urlpatterns = [
    path('admin/parcels/', parcel_type_list_view, name='list'),
    path('admin/parcels/create/', parcel_type_create_view, name='create'),
    path('admin/parcels/delete/<int:parcel_type_id>/', parcel_type_delete_view, name='delete'),
]
