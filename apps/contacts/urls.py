"""
URL configuration for contacts app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContactViewSet, IndustryViewSet,
    contact_list_view, contact_create_view, contact_import_view
)

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'industries', IndustryViewSet, basename='industry')

from .dashboard import dashboard_stats

app_name = 'contacts'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    path('api/dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    
    # Web-based views
    path('admin/contacts/', contact_list_view, name='list'),
    path('admin/contacts/create/', contact_create_view, name='create'),
    path('admin/contacts/import/', contact_import_view, name='import'),
]

