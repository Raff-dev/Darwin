import os
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from darwin.celery.tasks import create_embeddings_task
from darwin.web.api.documents import models, schemas
from darwin.web.database import engine, get_db
from darwin.web.settings import MEDIA_ROOT

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/", response_model=schemas.Document)
async def create_document(
    filename: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> models.Document | JSONResponse:
    if file.content_type != "application/pdf":
        return JSONResponse(
            status_code=400, content={"error": "Only PDF files are allowed."}
        )

    filepath = f"{MEDIA_ROOT}/{uuid.uuid4()}"
    with open(filepath, "wb") as f:
        data = await file.read()
        f.write(data)

    db_document = models.Document(filename=filename, filepath=filepath)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    create_embeddings_task.delay(filepath)
    return db_document


@router.get("/{document_id}", response_model=schemas.Document)
def read_document(document_id: int, db: Session = Depends(get_db)) -> models.Document:
    document = (
        db.query(models.Document).filter(models.Document.id == document_id).first()
    )
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/", response_model=list[schemas.Document])
def read_documents(db: Session = Depends(get_db)) -> list[models.Document]:
    documents = db.query(models.Document).all()
    if not documents:
        raise HTTPException(status_code=404, detail="Documents not found")
    return documents


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)) -> dict:
    db_document = (
        db.query(models.Document).filter(models.Document.id == document_id).first()
    )
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    filepath = db_document.filepath
    os.remove(filepath)
    db.delete(db_document)
    db.commit()
    return {"detail": "Document deleted"}