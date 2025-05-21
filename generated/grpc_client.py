import grpc
from generated.odds_engine_pb2 import (
    MatchStateRequest,
    BetRequest,
    OddsQueryRequest,
    SetInitialOddsRequest,
)
from generated.odds_engine_pb2_grpc import OddsEngineStub


class GRPCClient:
    def __init__(self, host="localhost", port=50051):
        channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = OddsEngineStub(channel)

    def set_initial_odds(self, game_id, market, initial_probability):
        request = SetInitialOddsRequest(
            game_id=game_id, market=market, initialProbability=initial_probability
        )
        return self.stub.SetInitialOdds(request)

    def update_match_state(self, match_state: dict):
        request = MatchStateRequest(
            gameId=match_state["gameId"],
            update=match_state["update"],  # must be a BallUpdate message
        )
        return self.stub.UpdateMatchState(request)

    def place_bet(self, bet_data: dict):
        request = BetRequest(
            gameId=bet_data["gameId"], bet=bet_data["bet"]  # must be a Bet message
        )
        return self.stub.PlaceBet(request)

    def get_latest_odds(self, game_id: str, market: str):
        request = OddsQueryRequest(gameId=game_id, market=market)
        return self.stub.GetOdds(request)
