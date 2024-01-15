from celery import shared_task

from darwin.chat import create_embeddings


@shared_task
def process_document(document_id: int, filepath: str):
    create_embeddings.process_document(document_id, filepath)
