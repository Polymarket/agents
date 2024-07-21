# import sys
# import os
# import json
# import devtools
# import requests
# from pathlib import Path
# from pprint import pprint
# from api.polymarket.polymarket import Polymarket
# from api.polymarket.gamma_market_client import GammaMarketClient
# from dotenv import load_dotenv
# from langchain_community.document_loaders import JSONLoader
# from langchain_text_splitters import RecursiveJsonSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_chroma import Chroma, vectorstores
# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate

# load_dotenv()

# openai_api_key = os.getenv("OPENAI_API_KEY")
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# client = GammaMarketClient()

# # JSON preprocesing step
# data = client.get_markets()


# # Function to convert custom objects to dictionaries
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
# pprint(data)

# # this split is rather arbitrary
# splitter = RecursiveJsonSplitter(max_chunk_size=300)

# # # Make splits. json splitter does not split lists by default
# texts = splitter.split_text(json_data=json_data, convert_lists=True)

# # # print([len(text) for text in texts][:10])

# persist_directory = "data/polymarket_db"

# # # Index
# embeddings = OpenAIEmbeddings()

# # # Index the texts using Chroma with the embeddings
# vectorstore = Chroma("polymarket_db", embeddings)

# vectorstore.from_texts(
#     texts=texts,
#     embeddings=embeddings,
#     persist_directory=persist_directory,
# )

# vectorstore()

# retriever = vectorstore.as_retriever()

# result = vectorstore.query(query_texts=["what's a market?"], n_results=2)
# pprint(result)


# template = """Anwswer the question based on the only the following context:
#     {context}

#     Question: {question}
# """

# prompt = ChatPromptTemplate.from_template(template)
# rag_chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParsers()
# )

# rag_chain.invoke("What is the X user market?")

# query = retriever.get_relevant_documents(
#     "What is a market about when x will charge users?"
# )

# Generation
