import os
import sys

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from redundant_filter_retriever import RedundantFilterRetriever

__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY)  # type: ignore

embeddings = OpenAIEmbeddings()

db = Chroma(persist_directory="embeddings", embedding_function=embeddings)

retriever = RedundantFilterRetriever(chroma=db, embeddings=embeddings)

chain = RetrievalQA.from_chain_type(retriever=retriever, llm=chat, chain_type="stuff")

result = chain("what is a fact about english language?")
print(result)
