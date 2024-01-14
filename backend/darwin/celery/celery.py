import os

from celery import Celery

broker_url = os.getenv("REDIS_URL")

celery_app = Celery("darwin", broker=broker_url)
