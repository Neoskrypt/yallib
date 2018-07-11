from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yallib.settings')
app = Celery("yallib")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace="CELERY")
app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(CELERY_TASK_RESULT_EXPIRES=3600, )
if __name__ == '__main__':
    app.start()
