import typer
from devtools import pprint

import pdb

from api.polymarket.polymarket import Polymarket
from ai.llm.prompts import generate_simple_ai_trader

app = typer.Typer()
polymarket = Polymarket()

@app.command()
def get_all_markets(limit: int = 5, sort_by: str = "volume"):
    print(f"limit: int = {limit}, sort_by: str = {sort_by}")
    markets = polymarket.get_all_markets()
    if (sort_by == "volume"):
        markets = sorted(markets, key=lambda x: x.volume, reverse=True)
    markets = markets[:limit]
    pprint(markets)

@app.command()
def get_relevant_news(event_description: str):
    print(f"event_description: str = {event_description}")

@app.command()
def evaluate_trade(market_summary: str, relevant_info: str):
    print(f"market_summary: str = {market_summary}, relevant_info: str = {relevant_info}")
    print(f"{generate_simple_ai_trader()}")

@app.command()
def execute_trade(market_id: int, price: int, ask_or_bid: str):
    print(f"market_id: int = {market_id}, price: int = {price}, ask_or_bid: str = {ask_or_bid}")

@app.command()
def create_market(market_description: str):
     print(f"market_description: str = {market_description}")


if __name__ == "__main__":
    app()
