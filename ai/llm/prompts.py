# interface for stitching prompts together


def generate_simple_ai_trader(market_description: str, relevant_info: str) -> str:
    return f"""
    
    You are a trader.
    
    Here is a market description: {market_description}.

    Here is relevant information: {relevant_info}.

    Do you buy or sell? How much?

    """


def get_sentiment_analysis(market_description: str, news_article: str):
    system_prompt = f"You are a sentiment analysis assistant. Analyze the sentiment of the given news articles for {market_description} and provide a summary of the overall sentiment and any notable changes over time. Be measured and discerning. You are a skeptical investor."
    news_text = ""
    for article in news:
        article_text = get_article_text(article["link"])
        timestamp = datetime.fromtimestamp(article["providerPublishTime"]).strftime(
            "%Y-%m-%d"
        )
        news_text += f"\n\n---\n\nDate: {timestamp}\nTitle: {article['title']}\nText: {article_text}"

    messages = [
        {
            "role": "user",
            "content": f"News articles for {ticker}:\n{news_text}\n\n----\n\nProvide a summary of the overall sentiment and any notable changes over time.",
        },
    ]

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 2000,
        "temperature": 0.5,
        "system": system_prompt,
        "messages": messages,
    }
    response = requests.post(
        "https://api.anthropic.com/v1/messages", headers=headers, json=data
    )
    response_text = response.json()["content"][0]["text"]

    return response_text
