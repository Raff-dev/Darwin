from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from darwin.web.database import Base


class MessageType(Enum):
    SYSTEM = "system"
    USER = "user"
    AI = "ai"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    type: Column = Column(SqlEnum(MessageType))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    conversation = relationship(Conversation, back_populates="messages")


Conversation.messages = relationship(
    Message, order_by=Message.id, back_populates="conversation"
)
