from __future__ import absolute_import, unicode_literals
from yallib.celery import app
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from yallib.utils import scrapers
from celery.utils.log import get_task_logger
from datetime import datetime


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def add(x, y):
    return x + y


@app.task(name="multyplay_two_numbers")
def mul(x, y):
    return x * y


logger = get_task_logger(__name__)
# A periodic task that will run every minute (the symbol "*" means every)


@periodic_task(run_every=crontab(hour=7, minute=38, day_of_week=1))
def scraper_example():
    logger.info("Start task")
    now = datetime.now()
    result = scrapers.scraper_example(now.day, now.minute)
    logger.info("Task finished: result = %i" % result)
