from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from darwin.chat import chat
from darwin.web.api.conversations import schemas
from darwin.web.api.conversations.models import Conversation, Message
from darwin.web.database import get_db

router = APIRouter()


@router.get("/{conversation_id}", response_model=list[schemas.Conversation])
def get_conversation(
    conversation_id: int, session: Session = Depends(get_db)
) -> Conversation | None:
    return (
        session.query(Conversation).filter(Conversation.id == conversation_id).first()
    )


@router.get("/{conversation_id}/messages", response_model=list[schemas.Message])
def get_messages(
    conversation_id: int, session: Session = Depends(get_db)
) -> list[Message]:
    return (
        session.query(Message).filter(Message.conversation_id == conversation_id).all()
    )


@router.post("/{conversation_id}/messages", response_model=schemas.Message)
async def create_conversation_message(
    message: schemas.MessageCreate,
    conversation_id: int,
    session: Session = Depends(get_db),
) -> StreamingResponse:
    conversation = (
        session.query(Conversation).filter(Conversation.id == conversation_id).first()
    )
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    async def stream_tokens() -> AsyncGenerator[str | Message, None]:
        for token in chat.ask_document(
            conversation=conversation,
            text=message.text,
        ):
            yield token

    return StreamingResponse(stream_tokens(), media_type="text/event-stream")
