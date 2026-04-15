"""
Paper trading v3 — demonstrates the full pipeline end-to-end.
Relaxes the restricted filter for demo purposes since Polymarket
geofences most events.
"""

import logging
import sys
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("paper-trading")

sys.path.insert(0, os.path.dirname(__file__))

from agents.polymarket.gamma import GammaMarketClient
from agents.polymarket.polymarket import Polymarket
from agents.utils.objects import SimpleMarket, SimpleEvent

STEP_SEP = "=" * 70


def step(n, title):
    logger.info("\n%s\nSTEP %d: %s\n%s", STEP_SEP, n, title, STEP_SEP)


def main():
    logger.info("Starting paper trading run v3...\n")

    gamma = GammaMarketClient()
    poly = Polymarket()

    # ── Step 1: Fetch and filter events (relaxed for paper trading) ────
    step(1, "Fetching active events from Gamma API")

    raw_events = gamma.get_current_events(limit=100)
    logger.info("✅ Fetched %d active events from Gamma API", len(raw_events))

    # Parse through Polymarket model
    all_events = []
    for e in raw_events:
        try:
            ed = poly.map_api_to_event(e)
            all_events.append(SimpleEvent(**ed))
        except Exception as ex:
            logger.debug("Skipping event: %s", ex)

    # Relaxed filter: active + not closed + not archived (skip restricted for demo)
    paper_tradeable = [
        e for e in all_events
        if e.active and not e.closed and not e.archived
    ]
    logger.info("Events passing paper-trade filter: %d", len(paper_tradeable))

    if paper_tradeable:
        logger.info("\nTop tradeable events:")
        for e in paper_tradeable[:10]:
            n_markets = len(e.markets.split(",")) if e.markets else 0
            logger.info(
                "  - [%d] %s (%d markets, volume=%.0f)",
                e.id,
                e.title[:65],
                n_markets,
                0,  # SimpleEvent doesn't have volume
            )

    # ── Step 2: Fetch market details for top events ────────────────────
    step(2, "Fetching market details for top events")

    markets_data = []
    for event in paper_tradeable[:5]:
        if not event.markets:
            continue
        market_ids = event.markets.split(",")[:2]  # Max 2 per event
        for mid in market_ids:
            mid = mid.strip()
            if not mid:
                continue
            try:
                raw = gamma.get_market(mid)
                m = poly.map_api_to_market(raw)
                markets_data.append(m)
            except Exception as ex:
                logger.debug("Skipping market %s: %s", mid, ex)

    logger.info("✅ Fetched %d market details", len(markets_data))

    # ── Step 3: Display market analysis ────────────────────────────────
    step(3, "Market analysis (what the agent evaluates)")

    for i, m in enumerate(markets_data[:10]):
        question = m.get("question", "N/A")
        outcomes = m.get("outcomes", "N/A")
        prices = m.get("outcome_prices", "N/A")
        active = m.get("active", False)
        funded = m.get("funded", False)
        spread = m.get("spread", "N/A")

        # Parse outcome prices for analysis
        try:
            price_list = eval(prices) if isinstance(prices, str) else prices
            yes_price = float(price_list[0]) if price_list else 0
            no_price = float(price_list[1]) if len(price_list) > 1 else 0
        except:
            yes_price = 0
            no_price = 0

        # Simple edge detection
        logger.info(
            "\n  📊 Market %d: %s\n"
            "     Outcomes: %s\n"
            "     Current prices: Yes=%.3f (%.1f%%) | No=%.3f (%.1f%%)\n"
            "     Active: %s | Funded: %s | Spread: %s\n"
            "     💡 Agent would run Superforecaster prompt to assess if "
            "the market is mispriced vs its base rate",
            i + 1,
            question[:80],
            outcomes,
            yes_price, yes_price * 100,
            no_price, no_price * 100,
            active, funded, spread,
        )

    # ── Step 4: What a paper trade would look like ─────────────────────
    step(4, "Paper trade example (simulated)")

    if markets_data:
        m = markets_data[0]
        question = m.get("question", "N/A")
        prices = m.get("outcome_prices", "['0.5','0.5']")

        try:
            price_list = eval(prices) if isinstance(prices, str) else prices
            yes_price = float(price_list[0])
        except:
            yes_price = 0.5

        # Simulate what the agent would decide
        simulated_prediction = 0.6  # Agent thinks 60% chance of Yes
        edge = simulated_prediction - yes_price

        if edge > 0.05:
            action = "BUY"
            size = min(0.1, edge)  # Scale size by edge
            reasoning = f"Market underprices YES at {yes_price:.1%}, agent predicts {simulated_prediction:.0%}"
        elif edge < -0.05:
            action = "SELL"
            size = min(0.1, abs(edge))
            reasoning = f"Market overprices YES at {yes_price:.1%}, agent predicts {simulated_prediction:.0%}"
        else:
            action = "HOLD"
            size = 0
            reasoning = f"Market fairly priced at {yes_price:.1%}, agent predicts {simulated_prediction:.0%}"

        logger.info(
            "\n  🎯 Simulated paper trade:\n"
            "     Market: %s\n"
            "     Current Yes price: %.3f (%.1f%%)\n"
            "     Agent prediction: %.0f%%\n"
            "     Edge: %+.1f%%\n"
            "     Action: %s\n"
            "     Size: %.1f%% of portfolio\n"
            "     Reasoning: %s\n"
            "\n  🔒 This is a SIMULATION — no real trade executed.",
            question[:80],
            yes_price, yes_price * 100,
            simulated_prediction * 100,
            edge * 100,
            action,
            size * 100,
            reasoning,
        )

    # ── Step 5: Pipeline status ────────────────────────────────────────
    step(5, "Pipeline readiness")

    openai_key = os.getenv("OPENAI_API_KEY")
    poly_key = os.getenv("POLYGON_WALLET_PRIVATE_KEY")

    logger.info(
        "\n  Environment:\n"
        "    OPENAI_API_KEY: %s\n"
        "    POLYGON_WALLET_PRIVATE_KEY: %s\n"
        "\n  Pipeline stages completed:\n"
        "    ✅ Step 1: Fetch events from Gamma API\n"
        "    ✅ Step 2: Fetch market details\n"
        "    ✅ Step 3: Display market analysis\n"
        "    ✅ Step 4: Simulate paper trade\n"
        "\n  Pipeline stages requiring OPENAI_API_KEY:\n"
        "    %s RAG filter events (ChromaDB + embeddings)\n"
        "    %s RAG filter markets\n"
        "    %s Superforecaster LLM prediction\n"
        "    %s Trade decision generation\n"
        "\n  Pipeline stages requiring POLYGON_WALLET_PRIVATE_KEY:\n"
        "    %s USDC balance check\n"
        "    %s Order signing and execution\n"
        "\n  Trade execution: 🔒 DISABLED (paper trading mode)",
        "✅ Set" if openai_key else "❌ Not set",
        "✅ Set" if poly_key else "❌ Not set",
        "✅" if openai_key else "⏭️",
        "✅" if openai_key else "⏭️",
        "✅" if openai_key else "⏭️",
        "✅" if openai_key else "⏭️",
        "✅" if poly_key else "⏭️",
        "✅" if poly_key else "⏭️",
    )

    logger.info("\n%s\nPaper trading run complete. 0 real trades. 0 USDC risked.\n%s\n", STEP_SEP, STEP_SEP)


if __name__ == "__main__":
    main()
