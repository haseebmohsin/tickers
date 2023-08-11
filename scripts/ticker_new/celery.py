import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticker_new.settings')

app = Celery('ticker_new')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True