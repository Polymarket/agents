import ast
import json
import logging
import math
import os
import re
from typing import List, Dict, Any

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from agents.polymarket.gamma import GammaMarketClient as Gamma
from agents.connectors.chroma import PolymarketRAG as Chroma
from agents.utils.objects import SimpleEvent, SimpleMarket
from agents.application.prompts import Prompter
from agents.polymarket.polymarket import Polymarket

logger = logging.getLogger(__name__)

def retain_keys(data, keys_to_retain):
    if isinstance(data, dict):
        return {
            key: retain_keys(value, keys_to_retain)
            for key, value in data.items()
            if key in keys_to_retain
        }
    elif isinstance(data, list):
        return [retain_keys(item, keys_to_retain) for item in data]
    else:
        return data

class Executor:
    def __init__(
        self,
        default_model: str = None,
        api_key: str = None,
        base_url: str = None,
    ) -> None:
        load_dotenv()
        self.prompter = Prompter()

        # Support any OpenAI-compatible provider via env vars or args
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL")
        self.model = default_model or os.getenv("LLM_MODEL", "gpt-3.5-turbo-16k")

        llm_kwargs = {
            "model": self.model,
            "temperature": 0,
            "api_key": self.api_key,
        }
        if self.base_url:
            llm_kwargs["base_url"] = self.base_url

        self.llm = ChatOpenAI(**llm_kwargs)

        max_token_model = {
            "gpt-3.5-turbo-16k": 15000,
            "gpt-4-1106-preview": 95000,
            "gpt-4o-mini": 125000,
            "gpt-4o": 125000,
        }
        self.token_limit = max_token_model.get(self.model, 15000)

        self.gamma = Gamma()
        self.chroma = Chroma()
        self.polymarket = Polymarket()

    def get_llm_response(self, user_input: str) -> str:
        system_message = SystemMessage(content=str(self.prompter.market_analyst()))
        human_message = HumanMessage(content=user_input)
        messages = [system_message, human_message]
        result = self.llm.invoke(messages)
        return result.content

    def get_superforecast(
        self, event_title: str, market_question: str, outcome: str
    ) -> str:
        messages = self.prompter.superforecaster(
            description=event_title, question=market_question, outcome=outcome
        )
        result = self.llm.invoke(messages)
        return result.content


    def estimate_tokens(self, text: str) -> int:
        # This is a rough estimate. For more accurate results, consider using a tokenizer.
        return len(text) // 4  # Assuming average of 4 characters per token

    def process_data_chunk(self, data1: List[Dict[Any, Any]], data2: List[Dict[Any, Any]], user_input: str) -> str:
        system_message = SystemMessage(
            content=str(self.prompter.prompts_polymarket(data1=data1, data2=data2))
        )
        human_message = HumanMessage(content=user_input)
        messages = [system_message, human_message]
        result = self.llm.invoke(messages)
        return result.content


    def divide_list(self, original_list, i):
        # Calculate the size of each sublist
        sublist_size = math.ceil(len(original_list) / i)
        
        # Use list comprehension to create sublists
        return [original_list[j:j+sublist_size] for j in range(0, len(original_list), sublist_size)]
    
    def get_polymarket_llm(self, user_input: str) -> str:
        data1 = self.gamma.get_current_events()
        data2 = self.gamma.get_current_markets()
        
        combined_data = str(self.prompter.prompts_polymarket(data1=data1, data2=data2))
        
        # Estimate total tokens
        total_tokens = self.estimate_tokens(combined_data)
        
        # Set a token limit (adjust as needed, leaving room for system and user messages)
        token_limit = self.token_limit
        if total_tokens <= token_limit:
            # If within limit, process normally
            return self.process_data_chunk(data1, data2, user_input)
        else:
            # If exceeding limit, process in chunks
            chunk_size = len(combined_data) // ((total_tokens // token_limit) + 1)
            logger.info('total tokens %d exceeding llm capacity, now will split and answer', total_tokens)
            group_size = (total_tokens // token_limit) + 1 # 3 is safe factor
            keys_no_meaning = ['image','pagerDutyNotificationEnabled','resolvedBy','endDate','clobTokenIds','negRiskMarketID','conditionId','updatedAt','startDate']
            useful_keys = ['id','questionID','description','liquidity','clobTokenIds','outcomes','outcomePrices','volume','startDate','endDate','question','questionID','events']
            data1 = retain_keys(data1, useful_keys)
            cut_1 = self.divide_list(data1, group_size)
            cut_2 = self.divide_list(data2, group_size)
            cut_data_12 = zip(cut_1, cut_2)

            results = []

            for cut_data in cut_data_12:
                sub_data1 = cut_data[0]
                sub_data2 = cut_data[1]
                sub_tokens = self.estimate_tokens(str(self.prompter.prompts_polymarket(data1=sub_data1, data2=sub_data2)))

                result = self.process_data_chunk(sub_data1, sub_data2, user_input)
                results.append(result)
            
            combined_result = " ".join(results)
            
        
            
            return combined_result
    def filter_events(self, events: "list[SimpleEvent]") -> str:
        prompt = self.prompter.filter_events(events)
        result = self.llm.invoke(prompt)
        return result.content

    def filter_events_with_rag(self, events: "list[SimpleEvent]") -> str:
        prompt = self.prompter.filter_events()
        logger.info("... prompting ... %s", prompt)
        return self.chroma.events(events, prompt)

    def map_filtered_events_to_markets(
        self, filtered_events: "list[SimpleEvent]"
    ) -> "list[SimpleMarket]":
        markets = []
        for e in filtered_events:
            data = json.loads(e[0].json())
            market_ids = data["metadata"]["markets"].split(",")
            for market_id in market_ids:
                market_data = self.gamma.get_market(market_id)
                formatted_market_data = self.polymarket.map_api_to_market(market_data)
                markets.append(formatted_market_data)
        return markets

    def filter_markets(self, markets) -> "list[tuple]":
        prompt = self.prompter.filter_markets()
        logger.info("... prompting ... %s", prompt)
        return self.chroma.markets(markets, prompt)

    def source_best_trade(self, market_object) -> str:
        market_document = market_object[0].dict()
        market = market_document["metadata"]
        outcome_prices = ast.literal_eval(market["outcome_prices"])
        outcomes = ast.literal_eval(market["outcomes"])
        question = market["question"]
        description = market_document["page_content"]

        prompt = self.prompter.superforecaster(question, description, outcomes)
        logger.info("... prompting superforecaster: %s", prompt)
        result = self.llm.invoke(prompt)
        content = result.content
        logger.info("Superforecaster result: %s", content)

        prompt = self.prompter.one_best_trade(content, outcomes, outcome_prices)
        logger.info("... prompting trade: %s", prompt)
        result = self.llm.invoke(prompt)
        content = result.content
        logger.info("Trade result: %s", content)
        return content

    def format_trade_prompt_for_execution(self, best_trade: str) -> float:
        """Parse LLM trade output into a safe USDC amount.

        Expected format: 'price:0.5, size:0.1, side:BUY,'
        Returns: size_fraction * usdc_balance
        """
        data = best_trade.split(",")
        if len(data) < 2:
            raise ValueError(
                f"Trade output has unexpected format (need >=2 comma-separated parts): {best_trade!r}"
            )

        size_matches = re.findall(r"\d+\.?\d*", data[1])
        if not size_matches:
            raise ValueError(
                f"Could not extract size from trade output: {data[1]!r}"
            )

        size = float(size_matches[0])
        if not (0 < size <= 1):
            raise ValueError(
                f"Trade size {size} out of safe range (0, 1] — refusing to execute"
            )

        usdc_balance = self.polymarket.get_usdc_balance()
        amount = size * usdc_balance
        logger.info(
            "Trade size fraction: %.4f, USDC balance: %.2f, order amount: %.2f",
            size,
            usdc_balance,
            amount,
        )
        return amount

    def source_best_market_to_create(self, filtered_markets) -> str:
        prompt = self.prompter.create_new_market(filtered_markets)
        logger.info("... prompting market creation: %s", prompt)
        result = self.llm.invoke(prompt)
        content = result.content
        return content
