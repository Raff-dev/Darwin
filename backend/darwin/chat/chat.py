from darwin.chat.vector_stores.pinecone import build_retriever
from darwin.settings import OPENAI_API_KEY
from darwin.web.api.conversations.models import Conversation, Message
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


def ask_document(conversation: Conversation, message: Message):
    model = ChatOpenAI(api_key=OPENAI_API_KEY)
    retriever = build_retriever(int(conversation.document_id))
    documents = retriever.get_relevant_documents(str(message.text))

    content = "\n".join([document.page_content for document in documents])

    prompt = PromptTemplate(
        input_variables=["content", "question"],
        template="""
        Based on the following content, answer the question below.
        You can only use the content to answer the question.
        ---
        Content: {content}
        ---
        Question: {question}
        """,
    )

    chain = LLMChain(llm=model, prompt=prompt, output_key="text")
    result = chain({"content": content, "question": message.text})
    return result["text"]
