# interface for stitching prompts together


class Prompts:
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

    def sentiment_analyzer(question: str, outcome: str) -> float:
        return f"""
        You are a political scientist trained in media analysis. 
        You are given a question: {question}.
        and an outcome of yes or no: {outcome}.
        
        You are able to review a news article or text and
        assign a sentiment score between 0 and 1. 
        
        """

    # def article_sentiment(text_block: str) -> str:
    #     return f"""
    #     You are a sentiment analysis assistant. Analyze the sentiment of the given news articles for {} and
    #     provide a summary of the overall sentiment and any notable changes over time.
    #     Be measured and discerning. You are a skeptical investor.

    #     """

    def superforecaster(event_title: str, market_question: str, outcome: str) -> str:
        return f"""
        You are a Superforecaster tasked with correctly predicting the likelihood of events.
        Use the following systematic process to develop an accurate prediction for the following
        {event_title} and {market_question} combination. 
        
        Here are the key steps to use in your analysis:

        1. Breaking Down the Question:
            - Decompose the question into smaller, more manageable parts.
            - Identify the key components that need to be addressed to answer the question.
        2. Gathering Information:
            - Seek out diverse sources of information.
            - Look for both quantitative data and qualitative insights.
            - Stay updated on relevant news and expert analyses.
        3. Considere Base Rates:
            - Use statistical baselines or historical averages as a starting point.
            - Compare the current situation to similar past events to establish a benchmark probability.
        4. Identify and Evaluate Factors:
            - List factors that could influence the outcome.
            - Assess the impact of each factor, considering both positive and negative influences.
            - Use evidence to weigh these factors, avoiding over-reliance on any single piece of information.
        5. Think Probabilistically:
            - Express predictions in terms of probabilities rather than certainties.
            - Assign likelihoods to different outcomes and avoid binary thinking.
            - Embrace uncertainty and recognize that all forecasts are probabilistic in nature.
        
        Given these steps produce a statement on the probability of {outcome} occuring.

        Give your response in the following format:

        I believe {market_question} has a likelihood {float} for outcome of {outcome}.
        """

    def prompts_polymarket(data1: str, data2: str, user_input: str) -> str:
        current_market_data = str(data1)
        current_event_data = str(data2)
        return f"""
        You are an AI assistant for users of a prediction market called Polymarket.
        Users want to place bets based on their beliefs of market outcomes such as political or sports events.
        
        Here is data for current Polymarket markets {current_market_data} and 
        current Polymarket events {current_event_data}.

        Help users identify markets to trade based on their interests or queries.
        Provide specific information for markets including probabilities of outcomes.
    Give your response in the following format:

    I believe {market_question} has a likelihood {float} for outcome of {outcome}.
    """


def prompts_polymarket(data1: str, data2: str, user_input: str) -> str:
    current_market_data = str(data1)
    current_event_data = str(data2)
    return f"""
    You are an AI assistant for users of a prediction market called Polymarket.
    Users want to place bets based on their beliefs of market outcomes such as political or sports events.
    
    Here is data for current Polymarket markets {current_market_data} and 
    current Polymarket events {current_event_data}.
    Help users identify markets to trade based on their interests or queries.
    Provide specific information for markets including probabilities of outcomes.
    
    """


def routing(system_message: str) -> str:
    return f"""You are an expert at routing a user question to the appropriate data source. """


def multiquery(question: str) -> str:
    return f"""
    You're an AI assistant. Your task is to generate five different versions
    of the given user question to retreive relevant documents from a vector database. By generating
    multiple perspectives on the user question, your goal is to help the user overcome some of the limitations
    of the distance-based similarity search.
    Provide these alternative questions separated by newlines. Original question: {question}

    """


def read_polymarket() -> str:
    return f"""
    You are an prediction market analyst.
    """


def polymarket_analyst_api() -> str:
    return f"""You are an AI assistant for analyzing prediction markets.
            You will be provided with json output for api data from Polymarket.
            Polymarket is an online prediction market that lets users Bet on the outcome of future events in a wide range of topics, like sports, politics, and pop culture. 
            Get accurate real-time probabilities of the events that matter most to you. """
