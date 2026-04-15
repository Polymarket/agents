import logging
import shutil

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from agents.application.executor import Executor as Agent
from agents.polymarket.gamma import GammaMarketClient as Gamma
from agents.polymarket.polymarket import Polymarket

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


class Trader:
    def __init__(self):
        self.polymarket = Polymarket()
        self.gamma = Gamma()
        self.agent = Agent()

    def pre_trade_logic(self) -> None:
        self.clear_local_dbs()

    def clear_local_dbs(self) -> None:
        for db_dir in ("local_db_events", "local_db_markets"):
            try:
                shutil.rmtree(db_dir)
            except FileNotFoundError:
                pass
            except OSError as e:
                logger.warning("Failed to remove %s: %s", db_dir, e)

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
    def one_best_trade(self) -> None:
        """
        one_best_trade is a strategy that evaluates all events, markets, and orderbooks.

        Leverages all available information sources accessible to the autonomous agent
        then executes that trade without any human intervention.
        """
        self.pre_trade_logic()

        events = self.polymarket.get_all_tradeable_events()
        logger.info("1. FOUND %d EVENTS", len(events))

        filtered_events = self.agent.filter_events_with_rag(events)
        logger.info("2. FILTERED %d EVENTS", len(filtered_events))

        markets = self.agent.map_filtered_events_to_markets(filtered_events)
        logger.info("3. FOUND %d MARKETS", len(markets))

        filtered_markets = self.agent.filter_markets(markets)
        logger.info("4. FILTERED %d MARKETS", len(filtered_markets))

        if not filtered_markets:
            logger.warning("No markets passed filtering — skipping trade")
            return

        market = filtered_markets[0]
        best_trade = self.agent.source_best_trade(market)
        logger.info("5. CALCULATED TRADE %s", best_trade)

        amount = self.agent.format_trade_prompt_for_execution(best_trade)
        # Please refer to TOS before uncommenting: polymarket.com/tos
        # trade = self.polymarket.execute_market_order(market, amount)
        # logger.info("6. TRADED %s", trade)

    def maintain_positions(self):
        pass

    def incentive_farm(self):
        pass


if __name__ == "__main__":
    t = Trader()
    t.one_best_trade()
