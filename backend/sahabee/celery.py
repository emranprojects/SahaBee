from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from rollcall import constants

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('sahabee')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    'periodic_time_sheets_send': {
        'task': constants.TASK_SEND_ACTIVE_TIMESHEETS,
        'schedule': settings.ACTIVE_TIMESHEET_SEND_INTERVAL,
    },
}
