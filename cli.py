from ai.llm.prompts import generate_simple_ai_trader
import typer

app = typer.Typer()

@app.command()
def get_events(limit: int = 5, sort_by: str = "daily_vol"):
    print(f"limit: int = {limit}, sort_by: str = {sort_by}")

@app.command()
def get_relevant_news(event_description: str):
    print(f"event_description: str = {event_description}")

@app.command()
def evaluate_trade(market_summary: str, relevant_info: str):
    print(f"market_summary: str = {market_summary}, relevant_info: str = {market_summary}")
    print(f"{generate_simple_ai_trader()}")

@app.command()
def execute_trade(market_id: int, price: int, ask_or_bid: str):
    print(f"market_id: int = {market_id}, price: int = {price}, ask_or_bid: str = {ask_or_bid}")

@app.command()
def create_market(market_description: str):
     print(f"market_description: str = {market_description}")


if __name__ == "__main__":
    app()
