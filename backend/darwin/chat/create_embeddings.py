from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from darwin.chat.vector_stores.pinecone import vector_store


def create_embeddings_for_pdf(document_id: int, file_path: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    loader = PyPDFLoader(file_path)
    documents = loader.load_and_split(splitter)

    for document in documents:
        document.metadata = {
            "page": document.metadata["page"],
            "text": document.metadata["text"],
            "document_id": document_id,
        }

    vector_store.add_documents(documents)
