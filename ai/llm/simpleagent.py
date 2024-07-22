import os
from pathlib import Path
import sys
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from ai.llm.prompts import prompts
from api.polymarket.gamma_market_client import GammaMarketClient

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)


def get_llm_response(user_input: str) -> str:
    system_message = SystemMessage(content=str(Prompts.market_analyst))
    human_message = HumanMessage(content=user_input)
    messages = [system_message, human_message]
    result = llm.invoke(messages)
    return result.content


def get_superforecast(event_title: str, market_question: str, outcome: str) -> str:
    messages = Prompts.superforecaster(
        event_title=event_title, market_question=market_question, outcome=outcome
    )
    result = llm.invoke(messages)
    return result.content


def get_polymarket_llm(user_input: str) -> str:
    client = GammaMarketClient()
    data1 = client.get_current_events()
    data2 = client.get_current_markets()
    system_message = SystemMessage(
        content=str(prompts.prompts_polymarket(data1=data1, data2=data2))
    )
    human_message = HumanMessage(content=user_input)
    messages = [system_message, human_message]
    result = llm.invoke(messages)
    return result.content


# add prompts on market data and news data
