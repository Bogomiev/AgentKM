import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agent_mobile.settings')
app = Celery('Agent_mobile')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'exchange': {
        'task': 'Agent_mobile.apps.core.tasks.exchange_trade',
        'schedule': 30.0
    }
}