from polymarket.agents.ai.llm.executor import Executor as Agent
from polymarket.agents.api.polymarket.polymarket import Polymarket
from polymarket.agents.data.newspaper import Newspaper


class Trader:
    def __init__(self):
        self.polymarket = Polymarket()
        self.newspaper = Newspaper()
        self.agent = Agent()

    def one_best_trade(self):
        """

        one_best_trade is a strategy evaluates all events, markets, and orderbooks

        leverages all available information sources accessible to the autonomous agent

        then executes that trade without any human intervention

        """
        events = self.polymarket.get_all_events()
        events = self.agent.filter_events()
        markets = [self.polymarket.get_market(e) for e in events]
        markets = self.agent.filter_markets()
        orderbooks = [self.polymarket.get_orderbooks(m) for m in markets]
        orderbooks = self.agent.filter_orderbooks()
        best_trade = self.agent.source_best_trade(
            events, markets, orderbooks, self.newspaper
        )
        formatted_best_trade = self.agent.format_trade_prompt_for_execution(best_trade)
        return self.polymarket.execute_order(**formatted_best_trade)

    def maintain_positions(self):
        pass

    def incentive_farm(self):
        pass
