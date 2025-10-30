"""
Contacts app URLs
"""
from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.ContactListView.as_view(), name='list'),
    path('add/', views.ContactCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.ContactUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ContactDeleteView.as_view(), name='delete'),
    
    # Bulk operation API endpoints
    path('api/bulk-export/', views.bulk_export_api, name='bulk_export_api'),
    path('api/bulk-delete/', views.bulk_delete_api, name='bulk_delete_api'),
    path('api/bulk-update/', views.bulk_update_api, name='bulk_update_api'),
]

