import sys
import os
import json
import devtools
from pathlib import Path
from pprint import pprint
from dotenv import load_dotenv
import tiktoken

# from api.polymarket.polymarket import Polymarket
# from api.polymarket.gamma_market_client import GammaMarketClient
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma, vectorstores
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import JSONLoader, WebBaseLoader
from langchain_text_splitters import (
    RecursiveJsonSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.tools.retriever import create_retriever_tool

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

docs_splits = text_splitter.split_documents(docs_list)

vectorstore = Chroma.from_documents(
    documents=docs_splits,
    collection_name="rag-polymarket-docs",
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
)

retriever = vectorstore.as_retriever()

retriever_tool = create_retriever_tool(
    retriever, "retrieve_blog_posts", "Search and return information about Polymarket"
)

tools = [retriever_tool]
pprint(tools)


# def fetch_polymarket_data():
#     client = GammaMarketClient()

#     # Fetch all events
#     events = polymarket.get_all_events()

#     events_data = [event.__dict__ for event in events]
#     events_json = json.dumps(events_data)

#     # Create a blobloader instance and load the data
#     blob_loader = BlobLoader()
#     blob_loader.load_data(events_json)

#     return blob_loader

#     markets = GammaMarketClient.get_current_markets()
#     print(f"Fetched {len(markets)} markets")
#     for market in markets:
#         print(market)

# tradeable_markets = GammaMarketClient.filter_markets_for_trading(markets)
# print(f"Filtered to {len(tradeable_markets)} tradeable markets")
# for market in tradeable_markets:
#     print(market)

# tradeable_events = GammaMarketClient.filter_events_for_trading(events)
# print(f"Filtered to {len(tradeable_events)} tradeable events")
# for event in tradeable_events:
#     print(event)

# def index_len_polymarket_data():
#     embd = OpenAIEmbeddings()
#     query_result = embd.embed_query({user_input})
#     document_result = embd.embed_query()
#     result = len(query_result)
#     print(result)

# # def
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# splits = text_splitter.split_documents(data)


# if __name__ == "__main__":
#     fetch_polymarket_data()


# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# splits = text_splitter.split_documents(data)

# # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# # # # Retrieve and generate using relevant snippets of polymarket data object.
# retriever = vectorstore.as_retriever()

# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# response = rag_chain.invoke("What is Task Decomposition?")
# print(response)
