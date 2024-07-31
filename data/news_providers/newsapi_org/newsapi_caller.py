import json
import os
import pathlib
from dotenv import load_dotenv
from newsapi import NewsApiClient

from data_sources.news_providers.newsapi_org.types import Article

load_dotenv()


class NewsApiCaller:
    def __init__(self) -> None:
        self.configs = {
            "language": "en",
            "country": "us",
            "top_headlines": "https://newsapi.org/v2/top-headlines?country=us&apiKey=",
            "base_url": "https://newsapi.org/v2/",
        }

        self.categories = {
            "business",
            "entertainment",
            "general",
            "health",
            "science",
            "sports",
            "technology",
        }

        self.API = NewsApiClient(os.getenv("NEWSAPI_API_KEY"))

    def get_articles_for_cli_keywords(self, keywords):
        query_words = keywords.split(",")
        all_articles = self.get_articles_for_options(query_words)
        article_objects: list[Article] = []
        for _, articles in all_articles.items():
            for article in articles:
                article_objects.append(Article(**article))
        return article_objects

    def get_top_articles_for_market(self, market_object):
        return self.API.get_top_headlines(language="en", country="usa", q=None)

    def get_articles_for_options(self, market_options, date_start=None, date_end=None):
        all_articles = {}
        # Default to top articles if no start and end dates are given for search
        if not date_start and not date_end:
            for option in market_options:
                response_dict = self.API.get_top_headlines(
                    q=option.strip(),
                    language=self.configs["language"],
                    country=self.configs["country"],
                )
                articles = response_dict["articles"]
                all_articles[option] = articles
        else:
            for option in market_options:
                response_dict = self.API.get_everything(
                    q=option.strip(),
                    language=self.configs["language"],
                    country=self.configs["country"],
                    from_param=date_start,
                    to=date_end,
                )
                articles = response_dict["articles"]
                all_articles[option] = articles

        return all_articles

    def get_category(self, market_object) -> str:
        news_category = "general"
        market_category = market_object["category"]
        if market_category in self.categories:
            news_category = market_category
        return news_category
