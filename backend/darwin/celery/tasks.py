from celery import shared_task

from darwin.chat.create_embeddings import create_embeddings_for_pdf


@shared_task
def create_embeddings_task(document_id: int, filepath: str):
    create_embeddings_for_pdf(document_id, filepath)
