from sqlalchemy.orm import Session

from darwin.web.api.conversations import models, schemas


def get_conversation(db: Session, conversation_id: int) -> models.Conversation | None:
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.id == conversation_id)
        .first()
    )


def get_conversations(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Conversation]:
    return db.query(models.Conversation).offset(skip).limit(limit).all()


def create_conversation(
    db: Session, conversation: schemas.ConversationCreate
) -> models.Conversation:
    db_conversation = models.Conversation(**conversation.model_dump())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def get_messages(db: Session, skip: int = 0, limit: int = 100) -> list[models.Message]:
    return db.query(models.Message).offset(skip).limit(limit).all()


def create_conversation_message(
    db: Session, message: schemas.MessageCreate, conversation_id: int
) -> models.Message:
    db_message = models.Message(**message.model_dump(), conversation_id=conversation_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
