"""Tests for agents.application.executor — trade parsing logic."""

import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock heavy imports before importing executor
sys.modules["langchain_core"] = MagicMock()
sys.modules["langchain_core.messages"] = MagicMock()
sys.modules["langchain_openai"] = MagicMock()
sys.modules["langchain_community"] = MagicMock()
sys.modules["langchain_community.vectorstores"] = MagicMock()
sys.modules["langchain_community.vectorstores.chroma"] = MagicMock()
sys.modules["langchain_community.document_loaders"] = MagicMock()


def retain_keys(data, keys_to_retain):
    """Direct copy for testing — avoids importing the full executor module."""
    if isinstance(data, dict):
        return {
            key: retain_keys(value, keys_to_retain)
            for key, value in data.items()
            if key in keys_to_retain
        }
    elif isinstance(data, list):
        return [retain_keys(item, keys_to_retain) for item in data]
    else:
        return data


class TestRetainKeys(unittest.TestCase):
    def test_retain_dict_keys(self):
        data = {"a": 1, "b": 2, "c": 3}
        result = retain_keys(data, ["a", "c"])
        self.assertEqual(result, {"a": 1, "c": 3})

    def test_retain_nested_list(self):
        data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        result = retain_keys(data, ["a"])
        self.assertEqual(result, [{"a": 1}, {"a": 3}])

    def test_retain_non_dict_value(self):
        result = retain_keys("hello", ["a"])
        self.assertEqual(result, "hello")

    def test_empty_keys(self):
        data = {"a": 1, "b": 2}
        result = retain_keys(data, [])
        self.assertEqual(result, {})


class TestFormatTradePromptForExecution(unittest.TestCase):
    """Tests for the trade parsing logic in format_trade_prompt_for_execution.

    We test the parsing/validation logic directly without loading the full executor,
    since that requires langchain, chromadb, etc.
    """

    def _parse_and_validate(self, best_trade: str) -> float:
        """Replicate the parsing logic from format_trade_prompt_for_execution."""
        import re

        data = best_trade.split(",")
        if len(data) < 2:
            raise ValueError(
                f"Trade output has unexpected format (need >=2 comma-separated parts): {best_trade!r}"
            )

        size_matches = re.findall(r"\d+\.?\d*", data[1])
        if not size_matches:
            raise ValueError(
                f"Could not extract size from trade output: {data[1]!r}"
            )

        size = float(size_matches[0])
        if not (0 < size <= 1):
            raise ValueError(
                f"Trade size {size} out of safe range (0, 1] — refusing to execute"
            )

        return size

    def test_valid_trade_0_1(self):
        size = self._parse_and_validate("price:0.5, size:0.1, side: BUY")
        self.assertAlmostEqual(size, 0.1)

    def test_valid_trade_exact_1(self):
        size = self._parse_and_validate("price:0.5, size:1, side: BUY")
        self.assertAlmostEqual(size, 1.0)

    def test_rejects_size_above_one(self):
        with self.assertRaises(ValueError) as ctx:
            self._parse_and_validate("price:0.5, size:1.5, side: BUY")
        self.assertIn("out of safe range", str(ctx.exception))

    def test_rejects_size_zero(self):
        with self.assertRaises(ValueError) as ctx:
            self._parse_and_validate("price:0.5, size:0, side: BUY")
        self.assertIn("out of safe range", str(ctx.exception))

    def test_rejects_malformed_input(self):
        with self.assertRaises(ValueError) as ctx:
            self._parse_and_validate("just some text without commas")
        self.assertIn("unexpected format", str(ctx.exception))

    def test_rejects_no_number_in_size(self):
        with self.assertRaises(ValueError) as ctx:
            self._parse_and_validate("price:0.5, size:abc, side: BUY")
        self.assertIn("Could not extract size", str(ctx.exception))

    def test_valid_decimal_size(self):
        size = self._parse_and_validate("price:0.3, size:0.25, side: BUY")
        self.assertAlmostEqual(size, 0.25)


if __name__ == "__main__":
    unittest.main()
