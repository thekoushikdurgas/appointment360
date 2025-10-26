"""
URL configuration for users app
"""
from django.urls import path
from .views import user_list_view, user_create_view, user_edit_view, user_column_settings_view

app_name = 'users'

urlpatterns = [
    path('admin/users/', user_list_view, name='list'),
    path('admin/users/create/', user_create_view, name='create'),
    path('admin/users/<int:user_id>/edit/', user_edit_view, name='edit'),
    path('admin/users/<int:user_id>/column/', user_column_settings_view, name='column'),
]

