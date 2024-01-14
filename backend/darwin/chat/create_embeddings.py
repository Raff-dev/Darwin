from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from darwin.chat.vector_stores.pinecone import vector_store


def create_embeddings_for_pdf(file_path: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    loader = PyPDFLoader(file_path)
    documents = loader.load_and_split(splitter)
    vector_store.add_documents(documents)
