import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reisetur.settings')
app = Celery('reisetur')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
