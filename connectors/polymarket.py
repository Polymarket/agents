# core polymarket api
# https://github.com/Polymarket/py-clob-client/tree/main/examples

import os
import pdb
import time
import ast

from dotenv import load_dotenv

from web3 import Web3
from web3.constants import MAX_INT
from web3.middleware import geth_poa_middleware

import httpx
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from py_clob_client.constants import AMOY, POLYGON
from py_order_utils.builders import OrderBuilder
from py_order_utils.model import OrderData
from py_order_utils.signer import Signer
from py_clob_client.clob_types import OrderArgs
from py_clob_client.order_builder.constants import BUY

from connectors.objects import SimpleMarket, SimpleEvent

load_dotenv()


class Polymarket:
    def __init__(self):
        self.gamma_url = "https://gamma-api.polymarket.com"
        self.gamma_markets_endpoint = self.gamma_url + "/markets"
        self.gamma_events_endpoint = self.gamma_url + "/events"

        self.clob_url = "https://clob.polymarket.com"
        self.clob_auth_endpoint = self.clob_url + "/auth/api-key"

        self.chain_id = 137  # POLYGON
        self.private_key = os.getenv("POLYGON_WALLET_PRIVATE_KEY")
        self.polygon_rpc = "https://polygon-rpc.com"
        self.w3 = Web3(Web3.HTTPProvider(self.polygon_rpc))

        self.exchange_address = "0x4bfb41d5b3570defd03c39a9a4d8de6bd8b8982e"
        self.neg_risk_exchange_address = "0xC5d563A36AE78145C45a50134d48A1215220f80a"

        self._init_api_keys()
        self._init_approvals(False)  # set to True first time running this!

    def _init_api_keys(self):
        self.client = ClobClient(
            self.clob_url, key=self.private_key, chain_id=self.chain_id
        )
        self.credentials = self.client.create_or_derive_api_creds()
        self.client.set_api_creds(self.credentials)
        print(self.credentials)

    def _init_approvals(self, run=False):
        if not run:
            return

        rpc_url = self.polygon_rpc
        priv_key = self.private_key
        pub_key = self.get_address_for_private_key()
        chain_id = self.chain_id

        erc20_approve = """[{"constant": false,"inputs": [{"name": "_spender","type": "address" },{ "name": "_value", "type": "uint256" }],"name": "approve","outputs": [{ "name": "", "type": "bool" }],"payable": false,"stateMutability": "nonpayable","type": "function"}]"""
        erc1155_set_approval = """[{"inputs": [{ "internalType": "address", "name": "operator", "type": "address" },{ "internalType": "bool", "name": "approved", "type": "bool" }],"name": "setApprovalForAll","outputs": [],"stateMutability": "nonpayable","type": "function"}]"""

        usdc_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
        ctf_address = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045"

        web3 = Web3(Web3.HTTPProvider(rpc_url))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        nonce = web3.eth.get_transaction_count(pub_key)

        usdc = web3.eth.contract(address=usdc_address, abi=erc20_approve)
        ctf = web3.eth.contract(address=ctf_address, abi=erc1155_set_approval)

        # CTF Exchange
        raw_usdc_approve_txn = usdc.functions.approve(
            "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E", int(MAX_INT, 0)
        ).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
        signed_usdc_approve_tx = web3.eth.account.sign_transaction(
            raw_usdc_approve_txn, private_key=priv_key
        )
        send_usdc_approve_tx = web3.eth.send_raw_transaction(
            signed_usdc_approve_tx.raw_transaction
        )
        usdc_approve_tx_receipt = web3.eth.wait_for_transaction_receipt(
            send_usdc_approve_tx, 600
        )
        print(usdc_approve_tx_receipt)

        nonce = web3.eth.get_transaction_count(pub_key)

        raw_ctf_approval_txn = ctf.functions.setApprovalForAll(
            "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E", True
        ).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
        signed_ctf_approval_tx = web3.eth.account.sign_transaction(
            raw_ctf_approval_txn, private_key=priv_key
        )
        send_ctf_approval_tx = web3.eth.send_raw_transaction(
            signed_ctf_approval_tx.raw_transaction
        )
        ctf_approval_tx_receipt = web3.eth.wait_for_transaction_receipt(
            send_ctf_approval_tx, 600
        )
        print(ctf_approval_tx_receipt)

        nonce = web3.eth.get_transaction_count(pub_key)

        # Neg Risk CTF Exchange
        raw_usdc_approve_txn = usdc.functions.approve(
            "0xC5d563A36AE78145C45a50134d48A1215220f80a", int(MAX_INT, 0)
        ).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
        signed_usdc_approve_tx = web3.eth.account.sign_transaction(
            raw_usdc_approve_txn, private_key=priv_key
        )
        send_usdc_approve_tx = web3.eth.send_raw_transaction(
            signed_usdc_approve_tx.raw_transaction
        )
        usdc_approve_tx_receipt = web3.eth.wait_for_transaction_receipt(
            send_usdc_approve_tx, 600
        )
        print(usdc_approve_tx_receipt)

        nonce = web3.eth.get_transaction_count(pub_key)

        raw_ctf_approval_txn = ctf.functions.setApprovalForAll(
            "0xC5d563A36AE78145C45a50134d48A1215220f80a", True
        ).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
        signed_ctf_approval_tx = web3.eth.account.sign_transaction(
            raw_ctf_approval_txn, private_key=priv_key
        )
        send_ctf_approval_tx = web3.eth.send_raw_transaction(
            signed_ctf_approval_tx.raw_transaction
        )
        ctf_approval_tx_receipt = web3.eth.wait_for_transaction_receipt(
            send_ctf_approval_tx, 600
        )
        print(ctf_approval_tx_receipt)

        nonce = web3.eth.get_transaction_count(pub_key)

        # Neg Risk Adapter
        raw_usdc_approve_txn = usdc.functions.approve(
            "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296", int(MAX_INT, 0)
        ).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
        signed_usdc_approve_tx = web3.eth.account.sign_transaction(
            raw_usdc_approve_txn, private_key=priv_key
        )
        send_usdc_approve_tx = web3.eth.send_raw_transaction(
            signed_usdc_approve_tx.raw_transaction
        )
        usdc_approve_tx_receipt = web3.eth.wait_for_transaction_receipt(
            send_usdc_approve_tx, 600
        )
        print(usdc_approve_tx_receipt)

        nonce = web3.eth.get_transaction_count(pub_key)

        raw_ctf_approval_txn = ctf.functions.setApprovalForAll(
            "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296", True
        ).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
        signed_ctf_approval_tx = web3.eth.account.sign_transaction(
            raw_ctf_approval_txn, private_key=priv_key
        )
        send_ctf_approval_tx = web3.eth.send_raw_transaction(
            signed_ctf_approval_tx.raw_transaction
        )
        ctf_approval_tx_receipt = web3.eth.wait_for_transaction_receipt(
            send_ctf_approval_tx, 600
        )
        print(ctf_approval_tx_receipt)

    def get_api_key(self):
        return self.client.create_or_derive_api_creds()

    def get_all_markets(self) -> "list[SimpleMarket]":
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

    def filter_markets_for_trading(self, markets: "list[SimpleMarket]"):
        tradeable_markets = []
        for market in markets:
            if market.active and market.deployed:
                tradeable_markets.append(market)
        return tradeable_markets

    def get_market(self, token_id: str) -> SimpleMarket:
        params = {"clob_token_ids": token_id}
        res = httpx.get(self.gamma_markets_endpoint, params=params)
        if res.status_code == 200:
            data = res.json()
            market = data[0]
            return self.map_api_to_market(market, token_id)

    def map_api_to_market(self, market, token_id: str = "") -> SimpleMarket:
        market = {
            "id": int(market["id"]),
            "question": market["question"],
            "end": market["endDate"],
            "description": market["description"],
            "active": market["active"],
            # "deployed": market["deployed"],
            "funded": market["funded"],
            "rewardsMinSize": float(market["rewardsMinSize"]),
            "rewardsMaxSpread": float(market["rewardsMaxSpread"]),
            # "volume": float(market["volume"]),
            "spread": float(market["spread"]),
            "outcomes": str(market["outcomes"]),
            "outcome_prices": str(market["outcomePrices"]),
        }
        if token_id:
            market["token_id"] = token_id
        return market

    def get_all_events(self) -> "list[SimpleEvent]":
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
            "id": int(event["id"]),
            "ticker": event["ticker"],
            "slug": event["slug"],
            "title": event["title"],
            "description": event["description"],
            "active": event["active"],
            "closed": event["closed"],
            "archived": event["archived"],
            "new": event["new"],
            "featured": event["featured"],
            "restricted": event["restricted"],
            "end": event["endDate"],
            "markets": ",".join([x["id"] for x in event["markets"]]),
        }

    def filter_events_for_trading(self, events: "list[SimpleEvent]"):
        tradeable_events = []
        for event in events:
            if event.active and not event.restricted:
                tradeable_events.append(event)
        return tradeable_events

    def get_sampling_simplified_markets(self):
        markets = []
        raw_sampling_simplified_markets = self.client.get_sampling_simplified_markets()
        for raw_market in raw_sampling_simplified_markets["data"]:
            token_one_id = raw_market["tokens"][0]["token_id"]
            market = self.get_market(token_one_id)
            markets.append(market)
        return markets

    def get_orderbook(self, token_id: str):
        return self.client.get_order_book(token_id)

    def get_orderbook_price(self, token_id: str):
        return self.client.get_price(token_id)

    def get_address_for_private_key(self):
        account = self.w3.eth.account.from_key(str(self.private_key))
        return account.address

    def build_order(
        self,
        market_token: str,
        amount: float,
        nonce: str = str(round(time.time())),  # for cancellations
        side: str = "BUY",
        expiration: str = "0",  # timestamp after which order expires
    ):
        signer = Signer(self.private_key)
        builder = OrderBuilder(self.exchange_address, self.chain_id, signer)

        buy = side == "BUY"
        side = 0 if buy else 1
        maker_amount = amount if buy else 0
        taker_amount = amount if not buy else 0
        order_data = OrderData(
            maker=self.get_address_for_private_key(),
            tokenId=market_token,
            makerAmount=maker_amount,
            takerAmount=taker_amount,
            feeRateBps="1",
            nonce=nonce,
            side=side,
            expiration=expiration,
        )
        order = builder.build_signed_order(order_data)
        return order

    def execute_order(self, price, size, side, token_id):
        return self.client.create_and_post_order(
            OrderArgs(price=price, size=size, side=side, token_id=token_id)
        )


def test():
    host = "https://clob.polymarket.com"
    key = os.getenv("POLYGON_WALLET_PRIVATE_KEY")
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
    url = "https://gamma-com"
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


if __name__ == "__main__":
    load_dotenv()

    p = Polymarket()

    # k = p.get_api_key()
    # m = p.get_sampling_simplified_markets()

    # print(m)
    # m = p.get_market('11015470973684177829729219287262166995141465048508201953575582100565462316088')

    # t = m[0]['token_id']
    # o = p.get_orderbook(t)
    # pdb.set_trace()

    """
    
    (Pdb) pprint(o)
            OrderBookSummary(
                market='0x26ee82bee2493a302d21283cb578f7e2fff2dd15743854f53034d12420863b55', 
                asset_id='11015470973684177829729219287262166995141465048508201953575582100565462316088', 
                bids=[OrderSummary(price='0.01', size='600005'), OrderSummary(price='0.02', size='200000'), ...
                asks=[OrderSummary(price='0.99', size='100000'), OrderSummary(price='0.98', size='200000'), ...
            )
    
    """

    # https://polygon-rpc.com

    test_market_token_id = (
        "101669189743438912873361127612589311253202068943959811456820079057046819967115"
    )
    test_market_data = p.get_market(test_market_token_id)

    test_size = 0.0001
    test_side = BUY
    test_price = float(ast.literal_eval(test_market_data["outcome_prices"])[0])

    order = p.execute_order(
        test_price,
        test_size,
        test_side,
        test_market_token_id,
    )
