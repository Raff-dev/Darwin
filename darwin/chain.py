import os

from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI  # pylint: disable=no-name-in-module
from langchain.prompts import PromptTemplate

API_KEY = os.getenv("OPENAI_API_KEY")

llm = OpenAI(openai_api_key=API_KEY)

code_prompt = PromptTemplate(
    template="""
    Write a very short {language} function that will {task}.
    reply only with code snippet
    """,
    input_variables=["language", "task"],
)

test_prompt = PromptTemplate(
    template="""
    Write test for a {language} code: {code}.
    reply only with code snippet.
    """,
    input_variables=["language", "code"],
)

code_chain = LLMChain(llm=llm, prompt=code_prompt, output_key="code")
test_chain = LLMChain(llm=llm, prompt=test_prompt, output_key="test")


chain = SequentialChain(
    chains=[code_chain, test_chain],
    input_variables=["language", "task"],
    output_variables=["code", "test"],
)

result = chain(
    {
        "language": "python",
        "task": "return the sum of two numbers",
    }
)

print(result["test"])
