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
from langchain_community.document_loaders import JSONLoader, WebBaseLoader
from langchain_text_splitters import (
    RecursiveJsonSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma, vectorstores
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# client = GammaMarketClient()

# JSON preprocesing step
# data = client.get_markets()

urls = [
    "https://learn.polymarket.com/what-is-polymarket"
    "https://learn.polymarket.com/how-to-deposit"
    "https://learn.polymarket.com/making-your-first-trade"
    "https://learn.polymarket.com/using-the-order-book"
    "https://docs.polymarket.com/#introduction"
    "https://docs.polymarket.com/#introduction-2"
    "https://docs.polymarket.com/#system"
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)

# this split is rather arbitrary
# splitter = RecursiveJsonSplitter(max_chunk_size=300)

# # Make splits. json splitter does not split lists by default
# texts = splitter.split_text(json_data=json_data, convert_lists=True)

# # # print([len(text) for text in texts][:10])

# persist_directory = "data/polymarket_db"

# # Index

# # Index the texts using Chroma with the embeddings
vectorstore = Chroma("polymarket_db", embeddings)

vectorstore.from_texts(
    texts=texts,
    embeddings=embeddings,
    persist_directory=persist_directory,
)

vectorstore()

retriever = vectorstore.as_retriever()

result = vectorstore.query(query_texts=["what's a market?"], n_results=2)
pprint(result)


template = """You're an AI assistant. Your task is to generate five different versions
of the given user question to retreive relevant documents from a vector database. By generating
multiple perspectives on the user question, your goal is to help the user overcome some of the limitations
of the distance-based similarity search.
Provide these alternative questions separated by newlines. Original question: {question}"""

prompt = ChatPromptTemplate.from_template(template)
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParsers()
)

rag_chain.invoke("What is the X user market?")

query = retriever.get_relevant_documents(
    "What is a market about when x will charge users?"
)

# Function to convert custom objects to dictionaries
# def convert_to_dict(obj):
#     if isinstance(obj, list):
#         return [convert_to_dict(i) for i in obj]
#     elif isinstance(obj, dict):
#         return {k: convert_to_dict(v) for k, v in obj.items()}
#     elif hasattr(obj, "__dict__"):
#         return convert_to_dict(vars(obj))
#     else:
#         return obj

# data = convert_to_dict(data)
