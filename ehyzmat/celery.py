from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehyzmat.settings')

app = Celery('ehyzmat')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'advertisement_task': {
        'task': 'advertisement.tasks.advertisement_vip_task',
        'schedule': crontab(hour=0, minute=0),
    },
    'OTP_task': {
        'task': 'otp.tasks.otp_task',
        'schedule': crontab(),
    }

}

app.autodiscover_tasks()