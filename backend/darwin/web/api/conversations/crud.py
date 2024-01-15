from darwin.web.api.conversations import models, schemas
from darwin.web.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{conversation_id}", response_model=list[schemas.Conversation])
def get_conversation(
    conversation_id: int, db: Session = Depends(get_db)
) -> models.Conversation | None:
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.id == conversation_id)
        .first()
    )


@router.get("/{conversation_id}/messages", response_model=list[schemas.Message])
def get_messages(
    conversation_id: int, db: Session = Depends(get_db)
) -> list[models.Message]:
    return (
        db.query(models.Message)
        .filter(models.Message.conversation_id == conversation_id)
        .all()
    )


@router.post("/{conversation_id}/messages", response_model=schemas.Message)
def create_conversation_message(
    message: schemas.MessageCreate, conversation_id: int, db: Session = Depends(get_db)
) -> models.Message:
    db_message = models.Message(**message.model_dump(), conversation_id=conversation_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
