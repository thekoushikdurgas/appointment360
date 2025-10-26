"""
URL configuration for dashboard app
"""
from django.urls import path
from .views import index

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', index, name='index'),
]

