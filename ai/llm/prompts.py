# interface for stitching prompts together


def generate_simple_ai_trader(market_description: str, relevant_info: str) -> str:
    return f"""
    
    You are a trader.
    
    Here is a market description: {market_description}.

    Here is relevant information: {relevant_info}.

    Do you buy or sell? How much?

    """


def market_analyst() -> str:
    return f"""
    You are a market analyst that takes a description of an event and produces a market forecast. 
    Assign a probability estimate to the event occurring described by the user
    """
