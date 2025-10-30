"""
Celery configuration for contact_manager project.
"""
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('contact_manager')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in all Django apps
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

