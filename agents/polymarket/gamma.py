import json
import logging

import httpx

from agents.utils.objects import Market, PolymarketEvent, ClobReward, Tag

logger = logging.getLogger(__name__)

HTTP_TIMEOUT = 30.0  # seconds
MAX_PAGINATION_ITERATIONS = 100  # safety cap


class GammaMarketClient:
    def __init__(self):
        self.gamma_url = "https://gamma-api.polymarket.com"
        self.gamma_markets_endpoint = self.gamma_url + "/markets"
        self.gamma_events_endpoint = self.gamma_url + "/events"

    def parse_pydantic_market(self, market_object: dict) -> Market:
        try:
            if "clobRewards" in market_object:
                clob_rewards: list[ClobReward] = []
                for clob_rewards_obj in market_object["clobRewards"]:
                    clob_rewards.append(ClobReward(**clob_rewards_obj))
                market_object["clobRewards"] = clob_rewards

            if "events" in market_object:
                events: list[PolymarketEvent] = []
                for market_event_obj in market_object["events"]:
                    parsed = self.parse_nested_event(market_event_obj)
                    if parsed is not None:
                        events.append(parsed)
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
        except (KeyError, ValueError, TypeError) as err:
            logger.warning("[parse_market] Caught exception: %s", err)
            logger.debug("exception while handling object: %s", market_object)
            return None

    # Event parser for events nested under a markets api response
    def parse_nested_event(self, event_object: dict) -> PolymarketEvent:
        logger.debug("[parse_nested_event] called with: %s", event_object)
        try:
            if "tags" in event_object:
                tags: list[Tag] = []
                for tag in event_object["tags"]:
                    tags.append(Tag(**tag))
                event_object["tags"] = tags

            return PolymarketEvent(**event_object)
        except (KeyError, ValueError, TypeError) as err:
            logger.warning("[parse_event] Caught exception: %s", err)
            return None

    def parse_pydantic_event(self, event_object: dict) -> PolymarketEvent:
        try:
            if "tags" in event_object:
                tags: list[Tag] = []
                for tag in event_object["tags"]:
                    tags.append(Tag(**tag))
                event_object["tags"] = tags
            return PolymarketEvent(**event_object)
        except (KeyError, ValueError, TypeError) as err:
            logger.warning("[parse_event] Caught exception: %s", err)
            return None

    def get_markets(
        self, querystring_params=None, parse_pydantic=False, local_file_path=None
    ) -> "list[Market]":
        if querystring_params is None:
            querystring_params = {}

        if parse_pydantic and local_file_path is not None:
            raise ValueError(
                'Cannot use "parse_pydantic" and "local_file" params simultaneously.'
            )

        response = httpx.get(
            self.gamma_markets_endpoint,
            params=querystring_params,
            timeout=HTTP_TIMEOUT,
        )
        if response.status_code == 200:
            data = response.json()
            if local_file_path is not None:
                with open(local_file_path, "w+") as out_file:
                    json.dump(data, out_file)
            elif not parse_pydantic:
                return data
            else:
                markets: list[Market] = []
                for market_object in data:
                    parsed = self.parse_pydantic_market(market_object)
                    if parsed is not None:
                        markets.append(parsed)
                return markets
        else:
            logger.error(
                "Error response from Gamma API: HTTP %d", response.status_code
            )
            raise RuntimeError(
                f"Gamma markets API returned HTTP {response.status_code}"
            )

    def get_events(
        self, querystring_params=None, parse_pydantic=False, local_file_path=None
    ) -> "list[PolymarketEvent]":
        if querystring_params is None:
            querystring_params = {}

        if parse_pydantic and local_file_path is not None:
            raise ValueError(
                'Cannot use "parse_pydantic" and "local_file" params simultaneously.'
            )

        response = httpx.get(
            self.gamma_events_endpoint,
            params=querystring_params,
            timeout=HTTP_TIMEOUT,
        )
        if response.status_code == 200:
            data = response.json()
            if local_file_path is not None:
                with open(local_file_path, "w+") as out_file:
                    json.dump(data, out_file)
            elif not parse_pydantic:
                return data
            else:
                events: list[PolymarketEvent] = []
                for market_event_obj in data:
                    parsed = self.parse_pydantic_event(market_event_obj)
                    if parsed is not None:
                        events.append(parsed)
                return events
        else:
            raise RuntimeError(
                f"Gamma events API returned HTTP {response.status_code}"
            )

    def get_all_markets(self, limit=2) -> "list[Market]":
        return self.get_markets(querystring_params={"limit": limit})

    def get_all_events(self, limit=2) -> "list[PolymarketEvent]":
        return self.get_events(querystring_params={"limit": limit})

    def get_current_markets(self, limit=4) -> "list[Market]":
        return self.get_markets(
            querystring_params={
                "active": True,
                "closed": False,
                "archived": False,
                "limit": limit,
            }
        )

    def get_all_current_markets(self, limit=100) -> "list[Market]":
        offset = 0
        all_markets = []
        iteration = 0
        while iteration < MAX_PAGINATION_ITERATIONS:
            params = {
                "active": True,
                "closed": False,
                "archived": False,
                "limit": limit,
                "offset": offset,
            }
            market_batch = self.get_markets(querystring_params=params)
            all_markets.extend(market_batch)

            if len(market_batch) < limit:
                break
            offset += limit
            iteration += 1
        else:
            logger.warning(
                "Hit max pagination iterations (%d) fetching markets",
                MAX_PAGINATION_ITERATIONS,
            )

        return all_markets

    def get_current_events(self, limit=4) -> "list[PolymarketEvent]":
        return self.get_events(
            querystring_params={
                "active": True,
                "closed": False,
                "archived": False,
                "limit": limit,
            }
        )

    def get_clob_tradable_markets(self, limit=2) -> "list[Market]":
        return self.get_markets(
            querystring_params={
                "active": True,
                "closed": False,
                "archived": False,
                "limit": limit,
                "enableOrderBook": True,
            }
        )

    def get_market(self, market_id: int) -> dict:
        url = self.gamma_markets_endpoint + "/" + str(market_id)
        logger.debug("Fetching market: %s", url)
        response = httpx.get(url, timeout=HTTP_TIMEOUT)
        return response.json()


if __name__ == "__main__":
    gamma = GammaMarketClient()
    market = gamma.get_market("253123")
    from agents.polymarket.polymarket import Polymarket

    poly = Polymarket()
    market_obj = poly.map_api_to_market(market)
