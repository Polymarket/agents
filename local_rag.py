from langchain_community.document_loaders import JSONLoader
import json
# from pathlib import Path
import os
from devtools import pprint
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def truncate_json():
    with open('./examples/markets_open.json', 'r+') as open_file:
        data = json.load(open_file)
    
    output = []
    for i in range(10):
        output.append(data[i])
    # pprint(output)

    with open('./examples/ten_markets.json', 'w+') as out_file:
        json.dump(output, out_file)
    

def load_json_from_local(json_file_path):
    # markets_file_path = './examples/markets_open.json'
    # markets_data = json.loads(Path(markets_file_path).read_text())
    loader = JSONLoader(
         file_path=json_file_path,
         jq_schema='.[].description',
         text_content=False)
    loaded_docs = loader.load()
    # pprint(loaded_docs)

    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    # db2 = Chroma.from_documents(loaded_docs, embedding_function, persist_directory="./chroma_local_db")
    # db2 = Chroma.from_documents(loaded_docs, embedding_function)
    # query = "Which market has the highest volume?"
    # response_docs = db2.similarity_search(query)
    # pprint(response_docs)
    print("\n\n")
    db3 = Chroma(persist_directory="./chroma_local_db", embedding_function=embedding_function)
    response_docs2 = db3.similarity_search_with_score("Which document has the lowest volume?")
    pprint(response_docs2)

def run_query(query):
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    local_db = Chroma(persist_directory="./chroma_local_db", embedding_function=embedding_function)
    response_docs = local_db.similarity_search_with_score("Which document has the lowest volume?")
    pprint(response_docs)

# truncate_json()
load_json_from_local('./examples/ten_markets.json')
