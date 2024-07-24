import json
import os
from devtools import pprint
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader

from dotenv import load_dotenv

from api.polymarket.gamma_market_client import GammaMarketClient
from ai.utils import utils as ai_utils

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# TODO:
# 1. Pull available markets
# 2. Prompt to find a market to trade on
# 3. Prompt to find which side of the market to place a bet on
# 4. Execute the trade on that market

def generate_embeds_from_local_json(json_file_path):
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    loader = JSONLoader(
        file_path = json_file_path,
        jq_schema='.[].description',
        content_key='description',
    )
    embeds = loader.load()

    in_memory_db = Chroma.from_documents(embeds, embedding_function)
    pprint(embeds)

def load_json_from_local(json_file_path):
    loader = JSONLoader(
         file_path=json_file_path,
         jq_schema='.[].description',
         text_content=False)
    loaded_docs = loader.load()

    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    db2 = Chroma.from_documents(loaded_docs, embedding_function, persist_directory="./chroma_local_db")

def run_query_on_local_data(query):
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    local_db = Chroma(persist_directory="./chroma_local_db", embedding_function=embedding_function)
    response_docs = local_db.similarity_search_with_score(query=query)
    pprint(response_docs)