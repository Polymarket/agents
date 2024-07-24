from api.polymarket.gamma_market_client import GammaMarketClient

class PolymarketRAG:
    def __init__(self, local_db_directory=None, embedding_function=None) -> None:
        self.gamma_client = GammaMarketClient()
        self.local_db_directory = local_db_directory
        self.embedding_function = embedding_function
    
    def create_local_vector_db(self):
        pass
