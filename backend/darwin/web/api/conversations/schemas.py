from pydantic import BaseModel

from darwin.web.api.conversations.models import MessageType


class MessageBase(BaseModel):
    text: str
    type: MessageType


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    conversation_id: int

    class Config:
        orm_mode = True


class ConversationBase(BaseModel):
    pass


class ConversationCreate(ConversationBase):
    pass


class Conversation(ConversationBase):
    id: int
    messages: list[Message] = []

    class Config:
        orm_mode = True
