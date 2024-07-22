import json
import os
import pathlib
from dotenv import load_dotenv
from newsapi import NewsApiClient

from data.news_providers.newsapi_org.types import Article

load_dotenv()

class NewsApiCaller:
    def __init__(self) -> None:
        path = pathlib.Path(__file__).parent.resolve()
        with open(f"{path}/configs.json", "r+") as config_file:
            config_json = json.load(config_file)
            self.configs = config_json["news_api"]
        
        self.API = NewsApiClient(os.getenv("NEWSAPI_API_KEY"))
        self.categories = {"business", "entertainment", "general", "health", "science", "sports", "technology"}
    
    def get_articles_for_cli_keywords(self, keywords):
        print("keywords:", keywords)
        query_words = keywords.split(',')
        print("query_words:", query_words)
        all_articles = self.get_articles_for_options(query_words)

        article_objects: list[Article] = []

        for keyword, articles in all_articles.items():
            for article in articles:
                article_objects.append(Article(**article))
        
        return article_objects

    def get_top_articles_for_event(self, event_object):
        pass

    def get_top_articles_for_market(self, market_object):
        news_category = self.get_category(market_object)
        self.API.get_top_headlines(language='en', country='usa', q=None)
    
    def get_articles_for_options(self, market_options, date_start=None, date_end=None):
        all_articles = {}
        # Default to top articles if no start and end dates are given for search
        if not date_start and not date_end:
            for option in market_options:
                response_dict = self.API.get_top_headlines(q=option.strip(),
                                                  language=self.configs["language"],
                                                  country=self.configs["country"])
                articles = response_dict["articles"]
                all_articles[option] = articles
        else:
            for option in market_options:
                response_dict = self.API.get_everything(q=option.strip(),
                                                   language=self.configs["language"],
                                                   country=self.configs["country"],
                                                   from_param=date_start,
                                                   to=date_end)
                articles = response_dict["articles"]
                all_articles[option] = articles
        
        return all_articles

    def get_category(self, market_object) -> str:
        news_category = "general"
        market_category = market_object["category"]
        if market_category in self.categories:
            news_category = market_category
        else:
            # TODO: Send query to OpenAI that says "here is the list of possible categories"
            # TODO: Send follow-up request to OpenAI asking "which of those categories does 'Russia & Ukraine' or 'NBA Playoffs' relate to?"
            pass
        
        return news_category
