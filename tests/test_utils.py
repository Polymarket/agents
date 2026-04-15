"""Tests for agents.utils.utils — preprocessing functions."""

import json
import os
import tempfile
import unittest

from agents.utils.utils import parse_camel_case, preprocess_market_object, preprocess_local_json


class TestParseCamelCase(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(parse_camel_case("isActive"), "is active")

    def test_all_lower(self):
        self.assertEqual(parse_camel_case("hello"), "hello")

    def test_multiple_caps(self):
        self.assertEqual(parse_camel_case("enableOrderBook"), "enable order book")

    def test_empty(self):
        self.assertEqual(parse_camel_case(""), "")


class TestPreprocessMarketObject(unittest.TestCase):
    def test_adds_boolean_context(self):
        obj = {
            "description": "A market about rain.",
            "active": True,
            "funded": False,
        }
        result = preprocess_market_object(obj)
        self.assertIn("This market is active", result["description"])
        self.assertIn("This market is not funded", result["description"])

    def test_adds_volume_context(self):
        obj = {
            "description": "Test market.",
            "volume": 5000.0,
            "liquidity": 1200.0,
        }
        result = preprocess_market_object(obj)
        self.assertIn("current volume of 5000.0", result["description"])
        self.assertIn("current liquidity of 1200.0", result["description"])

    def test_preserves_description_field(self):
        obj = {"description": "Original description."}
        result = preprocess_market_object(obj)
        self.assertTrue(result["description"].startswith("Original description."))


class TestPreprocessLocalJson(unittest.TestCase):
    def test_preprocess_file(self):
        data = [
            {"description": "Market 1", "active": True},
            {"description": "Market 2", "funded": False},
        ]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            input_path = f.name

        try:
            preprocess_local_json(input_path, preprocess_market_object)

            output_path = input_path.replace(".json", "_preprocessed.json")
            self.assertTrue(os.path.exists(output_path))

            with open(output_path) as f:
                result = json.load(f)

            self.assertEqual(len(result), 2)
            self.assertIn("This market is active", result[0]["description"])
            self.assertIn("This market is not funded", result[1]["description"])
        finally:
            os.unlink(input_path)
            output_path = input_path.replace(".json", "_preprocessed.json")
            if os.path.exists(output_path):
                os.unlink(output_path)


if __name__ == "__main__":
    unittest.main()
