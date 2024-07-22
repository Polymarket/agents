import typer
from devtools import pprint

import pdb

from api.polymarket.polymarket import Polymarket
from ai.llm.prompts import generate_simple_ai_trader

from ai.llm.simpleagent import get_llm_response, get_superforecast

# from ai.llm.langchainagent import get_llm_response
from data.news_providers.newsapi_caller import NewsApiCaller

app = typer.Typer()
polymarket = Polymarket()
newsapi_client = NewsApiCaller()


@app.command()
def get_all_markets(limit: int = 5, sort_by: str = "volume"):
    print(f"limit: int = {limit}, sort_by: str = {sort_by}")
    markets = polymarket.get_all_markets()
    markets = polymarket.filter_markets_for_trading(markets)
    if sort_by == "volume":
        markets = sorted(markets, key=lambda x: x.volume, reverse=True)
    markets = markets[:limit]
    pprint(markets)


@app.command()
def get_relevant_news(keywords: str):
    articles = newsapi_client.get_articles_for_cli_keywords(keywords)
    pprint(articles)


@app.command()
def get_all_events(limit: int = 5, sort_by: str = "number_of_markets"):
    print(f"limit: int = {limit}, sort_by: str = {sort_by}")
    events = polymarket.get_all_events()
    events = polymarket.filter_events_for_trading(events)
    if sort_by == "number_of_markets":
        events = sorted(events, key=lambda x: len(x.markets), reverse=True)
    events = events[:limit]
    pprint(events)


# @app.command()
# def get_market(events: str):
#     response = gammamarketclient.
#     print(f"event: str = {event}")
#     events = polymarket.get_markets()


# Generate probability statement with estimate between 0 and 1
@app.command()
def ask_superforecaster(event_title: str, market_question: str, outcome: str):
    print(
        f"event: str = {event_title}, question: str = {market_question}, outcome (usually yes or no): str = {outcome}"
    )
    response = get_superforecast(
        event_title=event_title, market_question=market_question, outcome=outcome
    )
    print(f"Response:{response}")


@app.command()
def ask_expert(market_question: str) -> str:
    print(f"We are finding a list of experts for {market_question}")


@app.command()
def evaluate_trade(market_summary: str, relevant_info: str):
    print(
        f"market_summary: str = {market_summary}, relevant_info: str = {relevant_info}"
    )
    print(f"{generate_simple_ai_trader()}")


@app.command()
def execute_trade(market_id: int, price: int, ask_or_bid: str):
    print(
        f"market_id: int = {market_id}, price: int = {price}, ask_or_bid: str = {ask_or_bid}"
    )


@app.command()
def create_market(market_description: str):
    print(f"market_description: str = {market_description}")


@app.command()
def ask_llm(user_input: str):
    """
    Ask a question to the LLM and get a response.
    """
    response = get_llm_response(user_input)
    print(f"LLM Response: {response}")


@app.command()
def ask_polymarket_llm(user_input: str):
    """
    What types of markets do you want trade?
    """
    response = get_polymarket_llm(user_input=user_input)
    print(f"LLM + current markets&events response: {response}")


if __name__ == "__main__":
    app()
