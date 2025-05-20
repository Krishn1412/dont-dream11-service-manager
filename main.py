from fastapi import FastAPI, HTTPException
from api.models import (
    BetRequestModel,
    BetResponseModel,
    BallUpdateModel,
    SetInitialOddsModel,
    OddsQueryResponseModel,
    AckResponseModel,
)
from api.models import Bet
from core.game_registry import GameRegistry
from generated.grpc_client import GRPCClient

app = FastAPI()
grpc_client = GRPCClient()
game_registry = GameRegistry(grpc_client)


@app.post("/game/{game_id}/market/{market}/init", response_model=AckResponseModel)
def initialize_game(game_id: str, market: str, payload: SetInitialOddsModel):
    try:
        game_registry.add_market(game_id, market, payload.initialProbability)
        return AckResponseModel(success=True, message="Game and market initialized.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/match/{game_id}/{market}/update", response_model=OddsQueryResponseModel)
def update_match(game_id: str, market: str, update: BallUpdateModel):
    try:
        grpc_payload = {"gameId": game_id, "update": update.dict()}
        odds = grpc_client.update_match_state(grpc_payload)
        game_registry.update_odds(game_id, market, odds.winProbability)
        return OddsQueryResponseModel(winProbability=odds.winProbability)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/bet/{game_id}/{market}", response_model=BetResponseModel)
def place_bet(game_id: str, market: str, bet_request: BetRequestModel):
    try:
        bet_manager = game_registry.get_bet_manager(game_id, market)
        bet = Bet(
            user_id=bet_request.userId,
            stake=bet_request.stake,
            odds=bet_request.odds,
            market=bet_request.market,
            team_a=bet_request.teamA,
        )
        updated_odds = bet_manager.place_bet(bet)
        game_registry.add_bet(game_id, market, bet)
        return BetResponseModel(
            winProbability=updated_odds, exposure=bet_manager.exposure
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/odds/{game_id}/{market}", response_model=OddsQueryResponseModel)
def get_latest_odds(game_id: str, market: str):
    try:
        odds = grpc_client.get_latest_odds(game_id, market)
        return OddsQueryResponseModel(winProbability=odds.winProbability)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
