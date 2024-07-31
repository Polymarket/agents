from polymarket.agents.ai.llm.executor import Executor as Agent
from polymarket.agents.api.polymarket import Polymarket
from polymarket.agents.data.newspaper import Newspaper


class Creator:
    def __init__(self):
        self.polymarket = Polymarket()
        self.newspaper = Newspaper()
        self.agent = Agent()

    def one_best_market(self):
        """

        one_best_market is a strategy that evaluates all events, markets, and orderbooks

        leverages all available information sources accessible to the autonomous agent

        then executes that trade without any human intervention

        """
        events = self.polymarket.get_all_events()
        events = self.agent.filter_events()
        markets = [self.polymarket.get_market(e) for e in events]
        markets = self.agent.filter_markets()
        orderbooks = [self.polymarket.get_orderbooks(m) for m in markets]
        orderbooks = self.agent.filter_orderbooks()
        return self.agent.source_best_market_to_create(
            events, markets, orderbooks, self.newspaper
        )
        # TODO: format response into json api
