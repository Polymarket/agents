import json
import os
from devtools import pprint
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader

from dotenv import load_dotenv

from api.polymarket import gamma_market_client

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def truncate_json():
    with open('./examples/markets_old.json', 'r+') as open_file:
        data = json.load(open_file)
    
    output = []
    for i in range(20):
        new_description = preprocess_description(data[i])
        data[i]['description'] = new_description
        output.append(data[i])
    # pprint(output)

    with open('./examples/twenty_markets_old_preprocessed.json', 'w+') as out_file:
        json.dump(output, out_file)

def parse_key(key):
    output = ''
    for char in key:
        if char.isupper():
            output += ' '
            output += char.lower()
        else:
            output += char
    return output

def preprocess_description(market_object):
    description = market_object['description']

    for k, v in market_object.items():
        if k == 'description':
            continue
        if isinstance(v, bool):
            description += f' This market is{" not" if not v else ""} {parse_key(k)}.'
        
        if k in ['volume', 'liquidity']:
            description += f" This market has a current {k} of {v}."
        # if isinstance(v, float) or isinstance(v, int):
        #     description +=
    print('\n\ndescription:', description)

    return description

def preprocess_json(file_path):
    with open(file_path, 'r+') as open_file:
        data = json.load(open_file)
    
    output = []
    for market in data:
        new_description = preprocess_description(market)
        market['description'] = new_description
        output.append(market)
    
    split_path = file_path.split('.')
    new_file_path = split_path[0] + "_preprocessed.json"
    with open(new_file_path, 'w+') as out_file:
        json.dump(output, out_file)

# Options for improving search:
# 1. Translate JSON params into natural language
# 2. Metadata function
# 3. Metadata function with post-filtering on metadata kv pairs
def metadata_func(record: dict, metadata: dict) -> dict:
    print('record:', record)
    print('meta:', metadata)
    for k, v in record.items():
        metadata[k] = v
    
    del metadata['description']
    del metadata['events']

    return metadata

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
    # pprint(loaded_docs)

    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    db2 = Chroma.from_documents(loaded_docs, embedding_function, persist_directory="./chroma_local_db")
    # db2 = Chroma.from_documents(loaded_docs, embedding_function)
    query = "Which market has the highest volume?"
    print("highest:")
    response_docs = db2.similarity_search_with_score(query=query)
    pprint(response_docs)
    print("\n\nlowest:")
    response_docs = db2.similarity_search_with_score(query="Which market has the lowest volume?")
    pprint(response_docs)
    # print("\n\n")
    # db3 = Chroma(persist_directory="./chroma_local_db", embedding_function=embedding_function)
    # response_docs2 = db3.similarity_search_with_score("Which document has the lowest volume?")
    # pprint(response_docs2)

def analyze_json():
    with open('./examples/ten_markets_preprocessed.json', 'r+') as open_file:
        data = json.load(open_file)
    
    out = []
    for market in data:
        out.append(market['volumeNum'])
    out.sort()
    pprint(out)

def run_query_on_local_data(query):
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    local_db = Chroma(persist_directory="./chroma_local_db", embedding_function=embedding_function)
    response_docs = local_db.similarity_search_with_score(query=query)
    pprint(response_docs)

# truncate_json()
# preprocess_json('./examples/markets_open.json')
# load_json_from_local('./examples/markets_old_preprocessed.json')
# analyze_json()
print('\nquery 1')
run_query_on_local_data("which markets are closed?")
print('\nquery 2')
run_query_on_local_data("which markets have low current volume?")
print('\nquery 3')
run_query_on_local_data("which markets have high current volume?")
print('\nquery 4')
run_query_on_local_data("which markets are not closed?")