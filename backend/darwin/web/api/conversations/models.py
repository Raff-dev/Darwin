from __future__ import annotations

from typing import Any

from langchain.schema.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from darwin.web.api.documents.models import Document
from darwin.web.database import Base, SessionLocal
from darwin.web.utils import MembershipEnum


class MessageType(MembershipEnum):
    SYSTEM = "system"
    HUMAN = "human"
    AI = "ai"
    FUNCTION = "function"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("Document", back_populates="conversations")

    @staticmethod
    def add_message(conversation_id: int, text: str, message_type: str):
        session = SessionLocal()
        if not MessageType.has_value(message_type):
            raise ValueError(f"Message type {message_type} not supported.")

        conversation = (
            session.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

        if not conversation:
            raise ValueError(f"Conversation with id {conversation_id} not found")

        enum_message_type = MessageType(message_type)
        db_message = Message(
            text=text, type=enum_message_type, conversation_id=conversation_id
        )
        conversation.messages.append(db_message)

        session.add(db_message)
        session.commit()
        session.close()


Document.conversations = relationship(
    Conversation, order_by=Conversation.id, back_populates="document"
)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    type: Any = Column(SqlEnum(MessageType))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    conversation = relationship(Conversation, back_populates="messages")

    @staticmethod
    def messages_from_conversation_id(
        conversation_id: int,
    ) -> list[BaseMessage]:
        session = SessionLocal()
        conversation = (
            session.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )
        if not conversation:
            raise ValueError(f"Conversation with id {conversation_id} not found")

        messages = [message.as_lc_message() for message in conversation.messages]
        session.close()
        return messages

    def as_lc_message(self) -> BaseMessage:
        text = str(self.text)
        if self.type == MessageType.HUMAN:
            return HumanMessage(content=text)
        if self.type in {MessageType.AI, MessageType.FUNCTION}:
            return AIMessage(content=text)
        if self.type == MessageType.SYSTEM:
            return SystemMessage(content=text)

        raise ValueError(f"Message type {self.type} not supported.")


Conversation.messages = relationship(
    Message, order_by=Message.id, back_populates="conversation"
)
