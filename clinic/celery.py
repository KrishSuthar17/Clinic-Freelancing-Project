import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic.settings')

app = Celery('clinic')

# Django settings se config lega
app.config_from_object('django.conf:settings', namespace='CELERY')

# tasks auto discover
app.autodiscover_tasks()
