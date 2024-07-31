import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from ai.llm import prompts
from api.polymarket.gamma import GammaMarketClient
from polymarket.agents.ai.llm.prompts import Prompter


class Executor:
    def __init__(self):
        load_dotenv()
        self.prompter = Prompter()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
        )

    def get_llm_response(self, user_input: str) -> str:
        system_message = SystemMessage(content=str(prompts.market_analyst))
        human_message = HumanMessage(content=user_input)
        messages = [system_message, human_message]
        result = self.llm.invoke(messages)
        return result.content

    def get_superforecast(
        self, event_title: str, market_question: str, outcome: str
    ) -> str:
        messages = prompts.superforecaster(
            event_title=event_title, market_question=market_question, outcome=outcome
        )
        result = self.llm.invoke(messages)
        return result.content

    def get_polymarket_llm(self, user_input: str) -> str:
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

    def filter_events(self):
        pass

    def filter_markets(self):
        pass

    def filter_orderbooks(self):
        pass

    def source_best_trade(self):
        pass

    def format_trade_prompt_for_execution(self):
        pass
