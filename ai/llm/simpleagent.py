import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["TAVILY_API_KEY"] = tavily_api_key

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)


def get_llm_response(user_input: str) -> str:
    messages = [
        SystemMessage(
            content="You are a market analyst that takes a description of an event and produce market forecast. Assign a probability estimate to the event occurring described by the user"
        ),
        HumanMessage(
            content="For the event: Joe Biden drops out of the 2024 US Presidential Race. What is the probability of that occuring? Here is my description: Joe Biden is an elder US politician. Over the last several weeks there have been several instances in which he appears to lose focus and train of thought. This has led to many in the public questioning his ability and fitness to serve as US president. He is currently down in the polls against his primary competitor for US President, Donald Trump."
        ),
    ]
    result = llm.invoke(messages)
    print(result)