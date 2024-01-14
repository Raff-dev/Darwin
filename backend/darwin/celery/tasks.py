from celery import shared_task

from darwin.chat.create_embeddings import create_embeddings_for_pdf


@shared_task
def create_embeddings_task(filepath):
    create_embeddings_for_pdf(filepath)
