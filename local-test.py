from api.polymarket.gamma_market_client import GammaMarketClient
from devtools import pprint

def test():
    client = GammaMarketClient()
    print(client)
    data = client.get_markets()
    pprint(data)

test()
