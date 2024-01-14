import os

from celery import Celery

broker_url = os.getenv("REDIS_URL")

app = Celery("darwin", broker=broker_url)
app.autodiscover_tasks()

from darwin.celery.tasks import *  # pylint: disable=all
