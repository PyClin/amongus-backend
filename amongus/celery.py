import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amongus.settings')

app = Celery('amongus')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
