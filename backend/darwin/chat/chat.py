from __future__ import annotations

from collections.abc import Generator

from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

from darwin.chat.chains.streamable import StreamableConversationRetrievalChain
from darwin.chat.database_memory import DatabaseChatMessageHistory
from darwin.chat.vector_stores.pinecone import vector_store
from darwin.settings import OPENAI_API_KEY
from darwin.web.api.conversations.models import Conversation


def ask_document(conversation: Conversation, text: str) -> Generator[str, None, None]:
    llm_35_turbo = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    llm_4_turbo = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4-1106-preview",
        streaming=True,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"filter": {"document_id": int(conversation.document_id)}}
    )

    memory = ConversationSummaryMemory.from_messages(
        chat_memory=DatabaseChatMessageHistory(
            conversation_id=int(conversation.id),
        ),
        memory_key="chat_history",
        output_key="answer",
        return_messages=True,
        llm=llm_35_turbo,
    )

    chain = StreamableConversationRetrievalChain.from_llm(
        llm=llm_4_turbo,
        memory=memory,
        retriever=retriever,
        condense_question_llm=llm_35_turbo,
        # verbose=True,
    )

    for chunk in chain.stream({"question": text}):
        yield chunk["token"]
