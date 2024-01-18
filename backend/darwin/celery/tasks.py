from sqlalchemy.orm import Session

from celery import shared_task
from darwin.chat import create_embeddings
from darwin.web.api.documents.models import Document, Status
from darwin.web.database import SessionLocal


@shared_task
def process_document(document_id: int, filepath: str):
    session: Session = SessionLocal()

    document = session.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise ValueError(f"Document with id {document_id} not found")

    document.status = Status.PROCESSING
    session.commit()

    try:
        create_embeddings.process_document(document_id, filepath)
        document.status = Status.PROCESSED
        session.commit()
    except Exception:
        document.status = Status.ERROR
        session.commit()
        raise
    finally:
        session.close()
