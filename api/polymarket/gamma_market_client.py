import httpx
import json
from devtools import pprint

from api.polymarket.types import PolymarketEvent
from api.polymarket.types import Market
from api.polymarket.types import ClobReward
from api.polymarket.types import Tag

class GammaMarketClient:
    def __init__(self):
        self.gamma_url = "https://gamma-api.polymarket.com"
        self.gamma_markets_endpoint = self.gamma_url + "/markets"
        self.gamma_events_endpoint = self.gamma_url + "/events"

    def parse_market(self, market_object):
        try:
            if "clobRewards" in market_object:
                clob_rewards: list[ClobReward] = []
                for clob_rewards_obj in market_object["clobRewards"]:
                    clob_rewards.append(ClobReward(**clob_rewards_obj))
                market_object["clobRewards"] = clob_rewards

            if "events" in market_object:
                events: list[PolymarketEvent] = []
                for market_event_obj in market_object["events"]:
                    events.append(self.parse_nested_event(market_event_obj))
                market_object["events"] = events

            # These two fields below are returned as stringified lists from the api
            if "outcomePrices" in market_object:
                market_object["outcomePrices"] = json.loads(
                    market_object["outcomePrices"]
                )
            if "clobTokenIds" in market_object:
                market_object["clobTokenIds"] = json.loads(
                    market_object["clobTokenIds"]
                )

            return Market(**market_object)
        except Exception as err:
            print(f"[parse_market] Caught exception: {err}")
            print("exception while handling object:", market_object)

    # Market parser for markets nested under an events api response
    def parse_nested_market(self, market_object):
        pass

    # Event parser for events nested under a markets api response
    def parse_nested_event(self, event_object):
        print("[parse_nested_event] called with:", event_object)
        try:
            if "tags" in event_object:
                print("tags here", event_object["tags"])
                tags: list[Tag] = []
                for tag in event_object["tags"]:
                    tags.append(Tag(**tag))
                event_object["tags"] = tags

            return PolymarketEvent(**event_object)
        except Exception as err:
            print(f"[parse_event] Caught exception: {err}")
            print("\n", event_object)

    def parse_event(self, event_object):
        try:
            if "tags" in event_object:
                print("tags here", event_object["tags"])
                tags: list[Tag] = []
                for tag in event_object["tags"]:
                    tags.append(Tag(**tag))
                event_object["tags"] = tags
            return PolymarketEvent(**event_object)
        except Exception as err:
            print(f"[parse_event] Caught exception: {err}")

    def get_markets(self, querystring_params={"limit": 2}):
        response = httpx.get(self.gamma_markets_endpoint, params=querystring_params)
        if response.status_code == 200:
            markets: list[Market] = []
            data = response.json()
            for market_object in data:
                markets.append(self.parse_market(market_object))
            return market_object
        else:
            print(f"Error response returned from api: HTTP {response.status_code}")
            raise Exception()

    def get_events(self, querystring_params={}):
        response = httpx.get(self.gamma_events_endpoint, params=querystring_params)
        if response.status_code == 200:
            events: list[PolymarketEvent] = []
            data = response.json()
            for market_event_obj in data:
                events.append(self.parse_event(market_event_obj))
            return events
        else:
            raise Exception()

    def get_all_markets(self, limit=2):
        return self.get_markets(querystring_params={"limit": limit})

    def get_all_events(self, limit=2):
        return self.get_events(querystring_params={"limit": limit})

    def get_current_markets(self, limit=2):
        return self.get_markets(
            querystring_params={
                "active": True,
                "closed": False,
                "archived": False,
                "limit": limit,
            }
        )

    def get_current_events(self, limit=2):
        return self.get_events(
            querystring_params={
                "active": True,
                "closed": False,
                "archived": False,
                "limit": limit,
            }
        )

    def get_clob_tradable_markets(self, limit=2):
        return self.get_markets(
            querystring_params={
                "active": True,
                "closed": False,
                "archived": False,
                "limit": limit,
                "enableOrderBook": True,
            }
        )
