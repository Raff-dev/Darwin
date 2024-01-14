import os

import pinecone
from langchain.vectorstores.pinecone import Pinecone

from darwin.chat.embeddings.openai import embeddings

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME"),
)

vector_store = Pinecone.from_existing_index(
    index_name=os.getenv("PINECONE_INDEX_NAME", ""),
    embedding=embeddings,
)
