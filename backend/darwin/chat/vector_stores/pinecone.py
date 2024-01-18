import pinecone  # pylint: disable=import-error
from langchain.vectorstores.pinecone import Pinecone

from darwin.chat.embeddings.openai import embeddings
from darwin.settings import PINECONE_API_KEY, PINECONE_ENV_NAME, PINECONE_INDEX_NAME

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV_NAME,
)

vector_store = Pinecone.from_existing_index(
    index_name=PINECONE_INDEX_NAME,
    embedding=embeddings,
)
