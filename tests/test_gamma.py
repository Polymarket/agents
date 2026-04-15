"""Tests for agents.polymarket.gamma — GammaMarketClient parsing logic."""

import unittest
from unittest.mock import patch, MagicMock

from agents.polymarket.gamma import GammaMarketClient


class TestGammaParsePydanticMarket(unittest.TestCase):
    def setUp(self):
        self.client = GammaMarketClient()

    def test_basic_market_parse(self):
        market_obj = {
            "id": 1,
            "question": "Will it rain?",
            "conditionId": "0xabc",
            "slug": "will-it-rain",
            "endDate": "2025-12-31",
            "startDate": "2025-01-01",
            "description": "A weather market",
            "active": True,
            "closed": False,
            "outcomePrices": '["0.3", "0.7"]',
            "clobTokenIds": '["tok1", "tok2"]',
        }
        result = self.client.parse_pydantic_market(market_obj)
        self.assertIsNotNone(result)
        self.assertEqual(result.question, "Will it rain?")
        self.assertEqual(result.outcomePrices, ["0.3", "0.7"])
        self.assertEqual(result.clobTokenIds, ["tok1", "tok2"])

    def test_market_with_clob_rewards(self):
        market_obj = {
            "id": 1,
            "question": "Test",
            "conditionId": "0xabc",
            "slug": "test",
            "endDate": "2025-12-31",
            "startDate": "2025-01-01",
            "description": "Test",
            "active": True,
            "closed": False,
            "outcomePrices": '["0.5", "0.5"]',
            "clobTokenIds": '["tok1", "tok2"]',
            "clobRewards": [
                {
                    "id": "1",
                    "conditionId": "0xabc",
                    "assetAddress": "0xdef",
                    "rewardsAmount": 0.0,
                    "rewardsDailyRate": 0,
                    "startDate": "2025-01-01",
                    "endDate": "2025-12-31",
                }
            ],
        }
        result = self.client.parse_pydantic_market(market_obj)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.clobRewards), 1)

    def test_malformed_market_returns_none(self):
        market_obj = {"bad_key": "bad_value"}
        result = self.client.parse_pydantic_market(market_obj)
        self.assertIsNone(result)


class TestGammaParseEvent(unittest.TestCase):
    def setUp(self):
        self.client = GammaMarketClient()

    def test_basic_event_parse(self):
        event_obj = {
            "id": "100",
            "title": "Election 2025",
            "active": True,
            "closed": False,
        }
        result = self.client.parse_pydantic_event(event_obj)
        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Election 2025")

    def test_event_with_tags(self):
        event_obj = {
            "id": "1",
            "title": "Test",
            "tags": [
                {"id": "1", "label": "Politics", "slug": "politics"},
            ],
        }
        result = self.client.parse_pydantic_event(event_obj)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.tags), 1)
        self.assertEqual(result.tags[0].label, "Politics")


class TestGammaGetMarkets(unittest.TestCase):
    @patch("agents.polymarket.gamma.httpx.get")
    def test_get_markets_returns_list(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1}, {"id": 2}]
        mock_get.return_value = mock_response

        client = GammaMarketClient()
        result = client.get_markets()
        self.assertEqual(len(result), 2)

    @patch("agents.polymarket.gamma.httpx.get")
    def test_get_markets_raises_on_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        client = GammaMarketClient()
        with self.assertRaises(RuntimeError):
            client.get_markets()


if __name__ == "__main__":
    unittest.main()
