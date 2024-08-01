import os
import time
import json

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from ai.llm import prompts
from api.gamma import GammaMarketClient
from ai.llm.prompts import Prompter
from ai.rag.chroma import Chroma


class Executor:

    def __init__(self):
        load_dotenv()
        self.prompter = Prompter()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
        )
        self.llm_embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        self.client = GammaMarketClient()
        self.chroma = Chroma()

        self.local_data_directory = "./localDb"
        if not os.path.isdir(self.local_data_directory):
            os.mkdir(self.local_data_directory)

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
        data1 = self.client.get_current_events()
        data2 = self.client.get_current_markets()
        system_message = SystemMessage(
            content=str(prompts.prompts_polymarket(data1=data1, data2=data2))
        )
        human_message = HumanMessage(content=user_input)
        messages = [system_message, human_message]
        result = self.llm.invoke(messages)
        return result.content

    def filter_events(self, events):
        if not self.chroma:
            # create local embedding for events
            local_events_embedding_path = f"{self.local_data_directory}/events.json"
            if os.path.isfile(self.local_data_directory):
                os.remove(local_events_embedding_path)
            with open(local_events_embedding_path, "w+") as output_file:
                json.dump(events, output_file)

            # load embedding into chroma
            local_db = Chroma(
                persist_directory=self.local_data_directory,
                embedding_function=self.llm_embedding_function,
            )

            # query using a prompt
            prompt = self.prompter.filter_events()
            print(prompt)
            response_docs = local_db.similarity_search_with_score(query=prompt)
            print(response_docs)
            return response_docs

        else:
            self.chroma.create_local_markets_rag()
            prompt = self.prompter.filter_events()
            return self.chroma.query_local_markets_rag(prompt)

    def filter_markets(self):
        pass

    def filter_orderbooks(self):
        pass

    def source_best_trade(self):
        pass

    def format_trade_prompt_for_execution(self):
        pass

    def source_best_market_to_create(self):
        pass
