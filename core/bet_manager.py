from generated.odds_engine_pb2 import Bet
from typing import Dict, Tuple, List
from concurrent.futures import ThreadPoolExecutor, as_completed


class BetManager:
    def __init__(self, game_id: str, market: str, grpc_client):
        self.game_id = game_id
        self.market = market
        self.grpc_client = grpc_client
        self.exposure = 0.0

    def place_bet(self, bet):
        self.exposure += bet.stake  # simplistic exposure logic
        grpc_bet = {
            "gameId": self.game_id,
            "bet": {
                "userId": bet.user_id,
                "stake": bet.stake,
                "odds": bet.odds,
                "market": bet.market,
                "teamA": bet.team_a,
            },
        }
        response = self.grpc_client.place_bet(grpc_bet)
        return response.winProbability
