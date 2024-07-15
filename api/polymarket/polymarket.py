# core polymarket api
# https://github.com/Polymarket/py-clob-client/tree/main/examples

import os
import pdb

import httpx
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from dotenv import load_dotenv
from py_clob_client.constants import AMOY

from api.polymarket.types import SimpleMarket

load_dotenv()

def auth():
    pass

def test():
    host = "https://clob.polymarket.com"
    key = os.getenv("PK")
    print(key)
    chain_id = POLYGON

    # Create CLOB client and get/set API credentials
    client = ClobClient(host, key=key, chain_id=chain_id)
    client.set_api_creds(client.create_or_derive_api_creds())

    creds = ApiCreds(
        api_key=os.getenv("CLOB_API_KEY"),
        api_secret=os.getenv("CLOB_SECRET"),
        api_passphrase=os.getenv("CLOB_PASS_PHRASE"),
    ) # TODO: post /auth/api-key
    chain_id = AMOY
    client = ClobClient(host, key=key, chain_id=chain_id, creds=creds)

    print(client.get_markets())
    print(client.get_simplified_markets())
    print(client.get_sampling_markets())
    print(client.get_sampling_simplified_markets())
    print(client.get_market("condition_id"))

    print("Done!")

def gamma():
    url = "https://gamma-api.polymarket.com"
    markets_url = url + "/markets"
    res = httpx.get(markets_url)
    code = res.status_code
    if (code == 200):
        markets: list[SimpleMarket] = []
        data = res.json()
        for market in data:
            try:
                market_data = {
                    "id": int(market['id']),
                    "question": market['question'],
                    # "start": market['startDate'],
                    "end": market['endDate'],
                    "description": market['description'],
                    "active": market['active'],
                    "deployed": market['deployed'],
                    "funded": market['funded'],
                    # "orderMinSize": float(market['orderMinSize']) if market['orderMinSize'] else 0,
                    # "orderPriceMinTickSize": float(market['orderPriceMinTickSize']),
                    "rewardsMinSize": float(market['rewardsMinSize']),
                    "rewardsMaxSpread": float(market['rewardsMaxSpread']),
                    "volume": float(market['volume']),
                    "spread": float(market['spread']),
                    "outcome_a": str(market['outcomes'][0]),
                    "outcome_b": str(market['outcomes'][1]),
                    "outcome_a_price": str(market['outcomePrices'][0]),
                    "outcome_b_price": str(market['outcomePrices'][1])
                }      
                markets.append(SimpleMarket(**market_data)) 
            except Exception as err:
                print(f'error {err} for market {id}')
        pdb.set_trace()
    else:
        raise Exception()
    

def main():
    # auth()
    # test()
    gamma()



if __name__ == "__main__":
    main()
