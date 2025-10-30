"""
Settings app URLs
"""
from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings_page, name='settings'),
    
    # API endpoints
    path('api/update/', views.update_user_settings, name='update_user_settings'),
    path('api/toggle-feature/<int:feature_id>/', views.toggle_feature, name='toggle_feature'),
    path('api/get-settings/', views.get_user_settings_api, name='get_user_settings_api'),
    
    # Settings management
    path('reset/', views.reset_settings, name='reset_settings'),
    path('export/', views.export_settings, name='export_settings'),
    path('import/', views.import_settings, name='import_settings'),
]
