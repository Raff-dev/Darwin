import pinecone  # pylint: disable=import-error
from darwin.chat.embeddings.openai import embeddings
from darwin.settings import PINECONE_API_KEY, PINECONE_ENV_NAME, PINECONE_INDEX_NAME
from langchain.vectorstores.pinecone import Pinecone
from langchain_core.vectorstores import VectorStoreRetriever

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV_NAME,
)

vector_store = Pinecone.from_existing_index(
    index_name=PINECONE_INDEX_NAME,
    embedding=embeddings,
)


def build_retriever(document_id: int) -> VectorStoreRetriever:
    search_kwargs = {"filter": {"document_id": document_id}}
    return vector_store.as_retriever(search_kwargs=search_kwargs)
