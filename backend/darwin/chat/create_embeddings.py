from darwin.chat.vector_stores.pinecone import vector_store
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def process_document(document_id: int, file_path: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    loader = PyPDFLoader(file_path)
    documents = loader.load_and_split(splitter)

    for document in documents:
        document.metadata = {
            "page": document.metadata["page"],
            "text": document.page_content,
            "document_id": document_id,
        }

    document_ids = vector_store.add_documents(documents)
    return document_ids
