import httpx
import logging

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from agents.application.executor import Executor as Agent
from agents.polymarket.gamma import GammaMarketClient as Gamma
from agents.polymarket.polymarket import Polymarket

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


class Creator:
    def __init__(self):
        self.polymarket = Polymarket()
        self.gamma = Gamma()
        self.agent = Agent()

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((
            ConnectionError,
            TimeoutError,
            RuntimeError,
            httpx.TimeoutException,
            httpx.NetworkError,
        )),
        reraise=True,
    )
    def one_best_market(self):
        """
        Evaluates all events, markets, and orderbooks using the autonomous agent,
        then proposes a new market idea.
        """
        events = self.polymarket.get_all_tradeable_events()
        logger.info("1. FOUND %d EVENTS", len(events))

        filtered_events = self.agent.filter_events_with_rag(events)
        logger.info("2. FILTERED %d EVENTS", len(filtered_events))

        markets = self.agent.map_filtered_events_to_markets(filtered_events)
        logger.info("3. FOUND %d MARKETS", len(markets))

        filtered_markets = self.agent.filter_markets(markets)
        logger.info("4. FILTERED %d MARKETS", len(filtered_markets))

        if not filtered_markets:
            logger.warning("No markets passed filtering — skipping")
            return None

        best_market = self.agent.source_best_market_to_create(filtered_markets)
        logger.info("5. IDEA FOR NEW MARKET %s", best_market)
        return best_market

    def maintain_positions(self):
        pass

    def incentive_farm(self):
        pass


if __name__ == "__main__":
    c = Creator()
    c.one_best_market()
