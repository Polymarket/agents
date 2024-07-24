import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

openai_api_key = os.getenv("OPEN_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key=tavily_api_key)

# Step 2. Executing a context search query
context = tavily_client.get_search_context(query="Will Biden drop out of the race?")
# Step 3. That's it! You now have a context string that you can feed directly into your RAG Application
