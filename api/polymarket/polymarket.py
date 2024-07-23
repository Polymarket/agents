# core polymarket api
# https://github.com/Polymarket/py-clob-client/tree/main/examples

import os
import pdb
from pprint import pprint

import httpx
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from dotenv import load_dotenv
from py_clob_client.constants import AMOY
from py_order_utils.builders import OrderBuilder
from py_order_utils.signer import Signer

from api.polymarket.types import SimpleMarket
from api.polymarket.types import SimpleEvent

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
    )  # TODO: post /auth/api-key
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
    if code == 200:
        markets: list[SimpleMarket] = []
        data = res.json()
        for market in data:
            try:
                market_data = {
                    "id": int(market["id"]),
                    "question": market["question"],
                    # "start": market['startDate'],
                    "end": market["endDate"],
                    "description": market["description"],
                    "active": market["active"],
                    "deployed": market["deployed"],
                    "funded": market["funded"],
                    # "orderMinSize": float(market['orderMinSize']) if market['orderMinSize'] else 0,
                    # "orderPriceMinTickSize": float(market['orderPriceMinTickSize']),
                    "rewardsMinSize": float(market["rewardsMinSize"]),
                    "rewardsMaxSpread": float(market["rewardsMaxSpread"]),
                    "volume": float(market["volume"]),
                    "spread": float(market["spread"]),
                    "outcome_a": str(market["outcomes"][0]),
                    "outcome_b": str(market["outcomes"][1]),
                    "outcome_a_price": str(market["outcomePrices"][0]),
                    "outcome_b_price": str(market["outcomePrices"][1]),
                }
                markets.append(SimpleMarket(**market_data))
            except Exception as err:
                print(f"error {err} for market {id}")
        pdb.set_trace()
    else:
        raise Exception()


def main():
    # auth()
    # test()
    # gamma()
    print(Polymarket().get_all_events())


class Polymarket:

    def __init__(self):
        self.gamma_url = "https://gamma-api.polymarket.com"
        self.gamma_markets_endpoint = self.gamma_url + "/markets"
        self.gamma_events_endpoint = self.gamma_url + "/events"

        self.clob_url = "https://clob.polymarket.com"
        self.clob_auth_endpoint = self.clob_url + "/auth/api-key"

        self.chain_id = 137 # POLYGON
        self.private_key = os.getenv("POLYGON_WALLET_PRIVATE_KEY")
        
        self._init_api_keys()

    def _init_api_keys(self):
        self.client = ClobClient(self.clob_url, key=self.private_key, chain_id=self.chain_id)
        self.credentials = self.client.create_or_derive_api_creds()
        self.client.set_api_creds(self.credentials)
        # print(self.credentials)

    def get_api_key(self):
        return self.client.create_or_derive_api_creds()

    def get_all_markets(self) -> list[SimpleMarket]:
        markets = []
        res = httpx.get(self.gamma_markets_endpoint)
        if res.status_code == 200:
            for market in res.json():
                try:
                    market_data = self.map_api_to_market(market)
                    markets.append(SimpleMarket(**market_data))
                except:
                    pass
        return markets

    def filter_markets_for_trading(self, markets: list[SimpleMarket]):
        tradeable_markets = []
        for market in markets:
            if market.active and market.deployed:
                tradeable_markets.append(market)
        return tradeable_markets

    def get_market(self, token_id: str) -> SimpleMarket:
        params = {
            "clob_token_ids": token_id
        }
        res = httpx.get(self.gamma_markets_endpoint, params=params)
        if (res.status_code == 200):
            data = res.json()
            market = data[0]
            return self.map_api_to_market(market, token_id)

    def map_api_to_market(self, market, token_id) -> SimpleMarket:
        market = {
            "id": int(market['id']),
            "question": market['question'],
            "end": market['endDate'],
            "description": market['description'],
            "active": market['active'],
            "deployed": market['deployed'],
            "funded": market['funded'],
            "rewardsMinSize": float(market['rewardsMinSize']),
            "rewardsMaxSpread": float(market['rewardsMaxSpread']),
            "volume": float(market['volume']),
            "spread": float(market['spread']),
            "outcomes": str(market['outcomes']),
            "outcome_prices": str(market['outcomePrices']),
        }
        if (token_id):
            market["token_id"] = token_id
        return market

    def get_all_events(self) -> list[SimpleEvent]:
        events = []
        res = httpx.get(self.gamma_events_endpoint)
        if res.status_code == 200:
            for event in res.json():
                try:
                    event_data = self.map_api_to_event(event)
                    events.append(SimpleEvent(**event_data))
                except:
                    pass
        return events

    def get_event(self):
        raise Exception()

    def map_api_to_event(self, event) -> SimpleEvent:
        return {
            "id": int(event['id']),
            "ticker": event['ticker'],
            "slug": event['slug'],
            "title": event['title'],
            "description": event['description'],
            "active": event['active'],
            "closed": event['closed'],
            "archived": event['archived'],
            "new": event['new'],
            "featured": event['featured'],
            "restricted": event['restricted'],
            "end": event['endDate'],
            "markets": ','.join([x['id'] for x in event['markets']]),
        }

    def filter_events_for_trading(self, events: list[SimpleEvent]):
        tradeable_events = []
        for event in events:
            if event.active and not event.restricted:
                tradeable_events.append(event)
        return tradeable_events

    def get_sampling_simplified_markets(self):
        markets = []
        raw_sampling_simplified_markets = self.client.get_sampling_simplified_markets()
        for raw_market in raw_sampling_simplified_markets['data']:
            token_one_id = raw_market['tokens'][0]['token_id']
            market = self.get_market(token_one_id)
            markets.append(market)
        return markets

    def get_orderbook(self, token_id: str):
        return self.client.get_order_book(token_id)

    def get_orderbook_price(self, token_id: str):
        return self.client.get_price(token_id)

    def build_order(self):
        exchange_address = "0x...."
        chain_id = 80002
        signer = Signer("0x....")
        builder = OrderBuilder(exchange_address, chain_id, signer)

        # Create and sign the order
        # order = builder.build_signed_order(
        #     OrderData(
        #         ...
        #     )
        # )

        # Generate the Order and Signature json to be sent to the CLOB API
        # pprint(json.dumps(order.dict()))

if __name__ == "__main__":
    p = Polymarket()
    k = p.get_api_key()
    m = p.get_sampling_simplified_markets()
    # print(m)
    # m = p.get_market('11015470973684177829729219287262166995141465048508201953575582100565462316088')
    t = m[0]['token_id']
    o = p.get_orderbook(t)
    pdb.set_trace()

    """
    
    (Pdb) pprint(o)
            OrderBookSummary(
                market='0x26ee82bee2493a302d21283cb578f7e2fff2dd15743854f53034d12420863b55', 
                asset_id='11015470973684177829729219287262166995141465048508201953575582100565462316088', 
                bids=[OrderSummary(price='0.01', size='600005'), OrderSummary(price='0.02', size='200000'), ...
                asks=[OrderSummary(price='0.99', size='100000'), OrderSummary(price='0.98', size='200000'), ...
            )
    
    """
