import logging
import os

from dotenv import load_dotenv
from tavily import TavilyClient

logger = logging.getLogger(__name__)

load_dotenv()

openai_api_key = os.getenv("OPEN_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")


def search_context(query: str) -> str:
    """Execute a Tavily context search and return the result string."""
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY environment variable is required")

    tavily_client = TavilyClient(api_key=tavily_api_key)
    context = tavily_client.get_search_context(query=query)
    return context


if __name__ == "__main__":
    result = search_context("Will Biden drop out of the race?")
    logger.info("Search result: %s", result)
