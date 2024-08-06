from application.executor import Executor as Agent
from connectors.gamma import GammaMarketClient as Gamma
from connectors.polymarket import Polymarket

import shutil


class Trader:
    def __init__(self):
        self.polymarket = Polymarket()
        self.gamma = Gamma()
        self.agent = Agent()

    def pre_trade_logic(self) -> None:
        self.clear_local_dbs()

    def clear_local_dbs(self) -> None:
        try:
            shutil.rmtree("local_db_events")
        except:
            pass
        try:
            shutil.rmtree("local_db_markets")
        except:
            pass

    def one_best_trade(self) -> None:
        """

        one_best_trade is a strategy that evaluates all events, markets, and orderbooks

        leverages all available information sources accessible to the autonomous agent

        then executes that trade without any human intervention

        """
        try:
            self.pre_trade_logic()

            events = self.polymarket.get_all_tradeable_events()
            print(f"1. FOUND {len(events)} EVENTS")

            filtered_events = self.agent.filter_events_with_rag(events)
            print(f"2. FILTERED {len(filtered_events)} EVENTS")

            markets = self.agent.map_filtered_events_to_markets(filtered_events)
            print()
            print(f"3. FOUND {len(markets)} MARKETS")

            print()
            filtered_markets = self.agent.filter_markets(markets)
            print(f"4. FILTERED {len(filtered_markets)} MARKETS")

            # TODO: use even more data to build even better models!
            # orderbooks = [self.polymarket.get_orderbooks(m) for m in markets]
            # orderbooks = self.agent.filter_orderbooks()

            market = filtered_markets[0]
            best_trade = self.agent.source_best_trade(market)
            print(f"5. CALCULATED TRADE {best_trade}")

            # TODO: explore more complex trading logic!
            amount = self.agent.format_trade_prompt_for_execution(best_trade)
            trade = self.polymarket.execute_market_order(market, amount)
            print(f"6. TRADED {trade}")

        except Exception as e:
            print(f"Error {e} \n \n Retrying")
            self.one_best_trade()

    def maintain_positions(self):
        pass

    def incentive_farm(self):
        pass


if __name__ == "__main__":
    t = Trader()
    t.one_best_trade()
