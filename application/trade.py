from application.executor import Executor as Agent
from connectors.gamma import GammaMarketClient as Gamma
from connectors.polymarket import Polymarket

import pdb
import json


class Trader:
    def __init__(self):
        self.polymarket = Polymarket()
        self.gamma = Gamma()
        self.agent = Agent()

    def one_best_trade(self):
        """

        one_best_trade is a strategy that evaluates all events, markets, and orderbooks

        leverages all available information sources accessible to the autonomous agent

        then executes that trade without any human intervention

        """
        try:
            events = self.polymarket.get_all_events()
            print(f"1. FOUND {len(events)} EVENTS")

            filtered_events = self.agent.filter_events_with_rag(events)
            print(f"2. FILTERED {len(filtered_events)} EVENTS")

            markets = self.agent.map_filtered_events_to_markets(filtered_events)
            print(f"3. FOUND {len(filtered_events)} MARKETS")

            filtered_markets = self.agent.filter_markets(markets)
            print(f"4. FILTERED {len(filtered_markets)} MARKETS")

            # orderbooks = [self.polymarket.get_orderbooks(m) for m in markets]
            # orderbooks = self.agent.filter_orderbooks()

            # best_trade = self.agent.source_best_trade(filtered_markets[0])
            # formatted_best_trade = self.agent.format_trade_prompt_for_execution(best_trade)

            # return self.polymarket.execute_order(**formatted_best_trade)
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
