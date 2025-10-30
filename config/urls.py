"""
URL configuration for contact_manager project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Root entry point - loading page
    path('', views.loading_view, name='home'),
    # Well-known endpoint for Chrome DevTools (prevents 404 noise)
    path('.well-known/appspecific/com.chrome.devtools.json', views.chrome_devtools_manifest, name='chrome_devtools_manifest'),
    # Core app URLs (includes welcome, dashboard, etc.)
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('contacts/', include('apps.contacts.urls')),
    path('imports/', include('apps.imports.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('exports/', include('apps.exports.urls')),
    path('jobs/', include('apps.jobs.urls')),
    path('settings/', include('apps.settings.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = 'Contact Manager Admin'
admin.site.site_title = 'Contact Manager'
admin.site.index_title = 'Administration'

