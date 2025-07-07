# project/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')

app = Celery('ADi-meals-mobile')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
