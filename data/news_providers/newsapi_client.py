import json
from newsapi import NewsApiClient
from newsapi import const
import urllib.parse


class NewsApiClient:
    def __init__(self) -> None:
        with open("./configs.json", "r+") as config_file:
            config_json = json.load(config_file)
            self.configs = config_json["news_api"]
        
        self.API = NewsApiClient(api_key=f'{self.configs["api_key"]}')
        self.categories = {"business", "entertainment", "general", "health", "science", "sports", "technology"}

    def get_top_articles_for_market(self, market_object):
        news_category = self.get_category(market_object)
        self.API.get_top_headlines(language='en')
    
    def get_articles_for_options(self, market_options, date_start=None, date_end=None):
        all_articles = {}
        # Default to top articles if no start and end dates are given for search
        if not date_start and not date_end:
            for option in market_options:
                print("\n[get_articles_for_options] No date range given. Searching top headlines.\n")
                response_dict = self.API.get_top_headlines(q=option,
                                                  language=self.configs["language"],
                                                  country=self.configs["country"])
                print(response_dict)
                articles = response_dict["articles"]
                all_articles[option] = articles
        else:
            for option in market_options:
                response_dict = self.API.get_everything(q=option,
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
        
    # TODO: parse query from polymarket market info, distill into queries, encode as url querystring
    def parse_query(self, market_info):
        query = market_info
        return query

def main():
    # print(const.CATEGORIES)
    print(const.CATEGORIES)
    exit()
    client = NewsApiQueryClient()
    # Placeholders for payload fetched from Polymarket
    market = "Presidential Election Winner 2024"
    options = [
        "Donald Trump",
        "Joe Biden",
        market,
        # "Kamala Harris",
        # "Michelle Obama",
        # "Other Democrat Politician",
    ]

    other_options = [
        "Donald Trump",
        "Joe Biden",
        "Kamala Harris",
        "Michelle Obama",
        "Other Democrat Politician",
    ]

    all_articles = client.get_articles_for_options(options)
    print(json.dumps(all_articles))
    # query_params = client.parse_query(market_title)

    # top_headlines = API.get_top_headlines(
    #     q=None,
    #     qintitle=None,
    #     sources=None,
    #     language = client.configs["language"],
    #     country = client.configs["country"],
    #     category=None,
    #     page_size=None,
    #     page=None)
    
    # all_articles = API.get_everything(
    #     q=None,
    #     qintitle=None,
    #     sources=None,
    #     domains=None,
    #     exclude_domains=None,
    #     from_param=None,
    #     to=None,
    #     language=None,
    #     sort_by=None,
    #     page=None,
    #     page_size=None)

main()