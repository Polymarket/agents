"""Tests for agents.application.prompts — prompt generation."""

import unittest
from agents.application.prompts import Prompter


class TestPrompter(unittest.TestCase):
    def setUp(self):
        self.p = Prompter()

    def test_market_analyst(self):
        result = self.p.market_analyst()
        self.assertIn("market analyst", result.lower())
        self.assertIn("probability", result.lower())

    def test_sentiment_analyzer(self):
        result = self.p.sentiment_analyzer("Will X win?", "Yes")
        self.assertIn("political scientist", result.lower())
        self.assertIn("Will X win?", result)
        self.assertIn("Yes", result)

    def test_prompts_polymarket(self):
        result = self.p.prompts_polymarket("market_data", "event_data")
        self.assertIn("market_data", result)
        self.assertIn("event_data", result)
        self.assertIn("prediction market", result.lower())

    def test_superforecaster(self):
        result = self.p.superforecaster(
            question="Will it rain?",
            description="Weather forecast says 80% chance.",
            outcome="Yes",
        )
        self.assertIn("Superforecaster", result)
        self.assertIn("Will it rain?", result)
        self.assertIn("Base Rates", result)

    def test_one_best_trade(self):
        result = self.p.one_best_trade(
            prediction="60% chance of Yes",
            outcomes=["Yes", "No"],
            outcome_prices="['0.4','0.6']",
        )
        self.assertIn("genius trade", result.lower())
        self.assertIn("price:", result.lower())
        self.assertIn("size:", result.lower())
        self.assertIn("side:", result.lower())

    def test_filter_events(self):
        result = self.p.filter_events()
        self.assertIn("Filter these events", result)

    def test_filter_markets(self):
        result = self.p.filter_markets()
        self.assertIn("Filter these markets", result)

    def test_multiquery(self):
        result = self.p.multiquery("Will AI take over?")
        self.assertIn("five different versions", result.lower())
        self.assertIn("Will AI take over?", result)

    def test_create_new_market(self):
        result = self.p.create_new_market("existing markets data")
        self.assertIn("Invent an information market", result)

    def test_routing(self):
        result = self.p.routing("some system message")
        self.assertIn("routing", result.lower())


if __name__ == "__main__":
    unittest.main()
