import json
import requests

class NewsClientFactory():
    def __init__(self) -> None:
        with open("./configs.json", "r+") as config_file:
            self.configs = json.load(config_file)

    def get_top_headlines(self):
        response = requests.get(self.configs["top_headlines"])
        data = response.json()
        print(json.dumps(data["articles"]))
    
    def get_market_genre(text):
        pass
    def get_relevant_news(text):
        pass


def main():
    client = NewsClient()
    client.get_headlines()

main()
