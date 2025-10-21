# project/celery.py
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')

app = Celery('my_site')
app.config_from_object('django.conf:settings', namespace='CELERYY')
app.autodiscover_tasks()#lambda: settings.INSTALLED_APPS)

