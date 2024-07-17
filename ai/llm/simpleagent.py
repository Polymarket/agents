import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from ai.llm import prompts

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)


def get_llm_response(user_input: str) -> str:
    system_message = SystemMessage(content=str(prompts.market_analyst))
    human_message = HumanMessage(content=user_input)
    messages = [system_message, human_message]
    result = llm.invoke(messages)
    return result.content


# add prompts on market data and news data
