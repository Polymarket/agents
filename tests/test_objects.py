"""Tests for agents.utils.objects — Pydantic model validation."""

import unittest
from agents.utils.objects import (
    SimpleMarket,
    SimpleEvent,
    Market,
    PolymarketEvent,
    Tag,
    ClobReward,
    Article,
    Source,
    Trade,
)


class TestSimpleMarket(unittest.TestCase):
    def test_valid_market(self):
        m = SimpleMarket(
            id=1,
            question="Will it rain?",
            end="2025-12-31",
            description="A weather market",
            active=True,
            funded=True,
            rewardsMinSize=0.0,
            rewardsMaxSpread=0.0,
            spread=0.05,
            outcomes="['Yes','No']",
            outcome_prices="['0.5','0.5']",
        )
        self.assertEqual(m.id, 1)
        self.assertTrue(m.active)

    def test_optional_clob_token_ids(self):
        m = SimpleMarket(
            id=1,
            question="Test",
            end="2025-01-01",
            description="desc",
            active=True,
            funded=True,
            rewardsMinSize=0.0,
            rewardsMaxSpread=0.0,
            spread=0.01,
            outcomes="['Yes','No']",
            outcome_prices="['0.5','0.5']",
            clob_token_ids="123,456",
        )
        self.assertEqual(m.clob_token_ids, "123,456")

    def test_missing_required_field_raises(self):
        with self.assertRaises(Exception):
            SimpleMarket(id=1)  # missing required fields


class TestSimpleEvent(unittest.TestCase):
    def test_valid_event(self):
        e = SimpleEvent(
            id=1,
            ticker="TEST",
            slug="test-event",
            title="Test Event",
            description="A test",
            end="2025-12-31",
            active=True,
            closed=False,
            archived=False,
            restricted=False,
            new=True,
            featured=False,
            markets="1,2,3",
        )
        self.assertEqual(e.id, 1)
        self.assertFalse(e.closed)
        self.assertEqual(e.markets, "1,2,3")


class TestMarket(unittest.TestCase):
    def test_minimal_market(self):
        m = Market(id=42)
        self.assertEqual(m.id, 42)
        self.assertIsNone(m.question)

    def test_full_market(self):
        m = Market(
            id=1,
            question="Will X happen?",
            conditionId="0xabc",
            slug="will-x-happen",
            description="desc",
            active=True,
            volume=1000.0,
            liquidity=500.0,
        )
        self.assertEqual(m.question, "Will X happen?")
        self.assertEqual(m.volume, 1000.0)


class TestPolymarketEvent(unittest.TestCase):
    def test_minimal_event(self):
        e = PolymarketEvent(id="100")
        self.assertEqual(e.id, "100")

    def test_event_with_tags(self):
        tag = Tag(id="1", label="Politics", slug="politics")
        e = PolymarketEvent(id="1", title="Election", tags=[tag])
        self.assertEqual(len(e.tags), 1)
        self.assertEqual(e.tags[0].label, "Politics")


class TestClobReward(unittest.TestCase):
    def test_reward(self):
        r = ClobReward(
            id="1",
            conditionId="0xabc",
            assetAddress="0xdef",
            rewardsAmount=0.0,
            rewardsDailyRate=0,
            startDate="2025-01-01",
            endDate="2025-12-31",
        )
        self.assertEqual(r.conditionId, "0xabc")


class TestTrade(unittest.TestCase):
    def test_trade(self):
        t = Trade(
            id=1,
            taker_order_id="abc",
            market="market1",
            asset_id="asset1",
            side="BUY",
            size="100",
            fee_rate_bps="1",
            price="0.5",
            status="matched",
            match_time="2025-01-01T00:00:00Z",
            last_update="2025-01-01T00:00:00Z",
            outcome="Yes",
            maker_address="0x123",
            owner="0x456",
            transaction_hash="0x789",
            bucket_index="0",
            maker_orders=["order1"],
            type="LIMIT",
        )
        self.assertEqual(t.side, "BUY")


class TestArticle(unittest.TestCase):
    def test_article(self):
        source = Source(id="1", name="Reuters")
        a = Article(
            source=source,
            author="John",
            title="Test Article",
            description="A test",
            url="https://example.com",
            urlToImage="https://example.com/img.png",
            publishedAt="2025-01-01T00:00:00Z",
            content="Full content here",
        )
        self.assertEqual(a.title, "Test Article")


if __name__ == "__main__":
    unittest.main()
