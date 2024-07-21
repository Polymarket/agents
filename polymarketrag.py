import sys
import os
import json
import devtools
import requests
from pathlib import Path
from pprint import pprint
from api.polymarket.polymarket import Polymarket
from api.polymarket.gamma_market_client import GammaMarketClient
from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma, vectorstores
from langchain_openai import ChatOpenAI


load_dotenv()


openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

question = "What is a market about when x will charge users?"

client = GammaMarketClient()

# JSON preprocesing step
json_data = client.get_markets()

# af: do we need tiktoken here to limit token input size?
splitter = RecursiveJsonSplitter(max_chunk_size=300)

# Make splits. json splitter does not split lists by default
texts = splitter.split_text(json_data=json_data, convert_lists=True)

# print the lengths of the first 10 splits to verify
print([len(text) for text in texts][:10])

# Index
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(texts=texts, embedding_function=embeddings)

retriever = vectorstore.as_retriever()

query = retriever.get_relevant_documents(
    "What is a market about when x will charge users?"
)
result = len(query)
pprint(result)
