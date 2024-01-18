from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage

from darwin.web.api.conversations.models import Conversation, Message


class DatabaseChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, conversation_id: int):
        self.conversation_id = conversation_id
        super().__init__()

    @property
    def messages(self) -> list[BaseMessage]:
        messages = Message.messages_from_conversation_id(
            conversation_id=self.conversation_id
        )
        return messages

    @messages.setter
    def messages(self, _: list[BaseMessage]) -> None:
        raise NotImplementedError("Cannot set messages on database chat history.")

    def add_message(self, message: BaseMessage) -> None:
        if not isinstance(message.content, str):
            raise ValueError("Message content must be a string.")

        Conversation.add_message(
            conversation_id=self.conversation_id,
            text=message.content,
            message_type=message.type,
        )

    def clear(self) -> None:
        pass
