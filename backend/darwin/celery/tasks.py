from darwin.celery.celery import celery_app
from darwin.chat.create_embeddings import create_embeddings_for_pdf


@celery_app.task
def create_embeddings_task(filepath):
    create_embeddings_for_pdf(filepath)
