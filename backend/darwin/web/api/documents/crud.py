import os
import uuid

from darwin.celery.tasks import process_document
from darwin.web.api.conversations import schemas as conversations_schemas
from darwin.web.api.conversations.models import Conversation
from darwin.web.api.documents import schemas as documents_schemas
from darwin.web.api.documents.models import Document
from darwin.web.database import get_db
from darwin.web.settings import MEDIA_ROOT
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

router = APIRouter()


@router.post("/", response_model=documents_schemas.Document)
async def create_document(
    filename: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> Document | JSONResponse:
    if file.content_type != "application/pdf":
        return JSONResponse(
            status_code=400, content={"error": "Only PDF files are allowed."}
        )

    filepath = f"{MEDIA_ROOT}/{uuid.uuid4()}"
    with open(filepath, "wb") as f:
        data = await file.read()
        f.write(data)

    db_document = Document(filename=filename, filepath=filepath)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    process_document.delay(db_document.id, filepath)
    return db_document


@router.get("/{document_id}", response_model=documents_schemas.Document)
def read_document(document_id: int, db: Session = Depends(get_db)) -> Document:
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/", response_model=list[documents_schemas.Document])
def read_documents(db: Session = Depends(get_db)) -> list[Document]:
    documents = db.query(Document).all()
    return documents


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)) -> dict:
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        os.remove(db_document.filepath)
    except OSError:
        pass

    db.delete(db_document)
    db.commit()
    return {"detail": "Document deleted"}


@router.get(
    "/{document_id}/conversations",
    response_model=list[conversations_schemas.Conversation],
)
def get_document_conversations(
    document_id: int, db: Session = Depends(get_db)
) -> list[Conversation]:
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return document.conversations


@router.post(
    "/{document_id}/conversations", response_model=conversations_schemas.Conversation
)
def create_document_conversation(
    document_id: int,
    conversation: conversations_schemas.ConversationCreate,
    db: Session = Depends(get_db),
) -> Conversation:
    db_conversation = Conversation(document_id=document_id, **conversation.model_dump())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation
