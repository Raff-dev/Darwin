import os
import sys

from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage

from darwin.course.agents.handlers.chat_model_start_handler import ChatModelStartHandler
from darwin.course.agents.tools.report import write_report_tool
from darwin.course.agents.tools.sql import (
    describe_table_tool,
    list_tables,
    run_query_tool,
)

__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

handler = ChatModelStartHandler()
chat = ChatOpenAI(
    api_key=OPENAI_API_KEY, callbacks=[handler], model="gpt-4-1106-preview"
)

tables = list_tables()
prompt = ChatPromptTemplate(
    input_variables=[],
    messages=[
        SystemMessage(
            content=f"""
            You are AI agent assisting in answering questions about the sqlite database.
            Following tables are available:
            {tables}
            You will not make assumptions about the schema of the tables.
            You will use tools available to gain information about the tables.
            """
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ],
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)
tools = [run_query_tool, describe_table_tool, write_report_tool]
agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools,
)
agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools, memory=memory)


agent_executor("How many orders are there? Write the result to a report")
agent_executor("Repeat the exact same process for users")
