import json
import os
import time
from devtools import pprint
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from api.polymarket.gamma_market_client import GammaMarketClient

class PolymarketRAG:
    def __init__(self, local_db_directory=None, embedding_function=None) -> None:
        self.gamma_client = GammaMarketClient()
        self.local_db_directory = local_db_directory
        self.embedding_function = embedding_function
    
    def load_json_from_local(self, json_file_path=None, vector_db_directory='./local_db'):
        loader = JSONLoader(
            file_path=json_file_path,
            jq_schema='.[].description',
            text_content=False)
        loaded_docs = loader.load()

        embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        db2 = Chroma.from_documents(loaded_docs, embedding_function, persist_directory=vector_db_directory)

        return db2

    def create_local_markets_rag(self, local_directory='./local_db'):
        all_markets = self.gamma_client.get_all_current_markets()

        if not os.path.isdir(local_directory):
            os.mkdir(local_directory)

        local_file_path = f'{local_directory}/all-current-markets_{time.time()}.json'

        with open(local_file_path, 'w+') as output_file:
            json.dump(all_markets, output_file)
        
        self.load_json_from_local(json_file_path=local_file_path, vector_db_directory=local_directory)
    
    def query_local_markets_rag(self, local_directory=None, query=None):
        embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        local_db = Chroma(persist_directory=local_directory, embedding_function=embedding_function)
        response_docs = local_db.similarity_search_with_score(query=query)
        return response_docs

# TODO:
# 1. Pull available markets
# 2. Prompt to find a market to trade on
# 3. Prompt to find which side of the market to place a bet on
# 4. Execute the trade on that market