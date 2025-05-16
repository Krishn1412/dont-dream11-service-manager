from api.models import Bet
from core.game_registry import GameRegistry
from api.models import BetRequestModel, BetResponseModel, BallUpdateModel, MatchStateRequestModel, SetInitialOddsModel, OddsQueryResponseModel, AckResponseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()
game_registry = GameRegistry()

@app.post("/bet/{game_id}/{market}", response_model=BetResponseModel)
def place_bet(game_id: str, market: str, bet_request: BetRequestModel):
    try:
        bet_manager = game_registry.get_bet_manager(game_id, market)
        bet = Bet(
            user_id=bet_request.userId,
            stake=bet_request.stake,
            odds=bet_request.odds,
            market=bet_request.market,
            team_a=bet_request.teamA
        )
        updated_probability = bet_manager.place_bet(bet)
        return BetResponseModel(
            winProbability=updated_probability,
            exposure=bet_manager.exposure
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/match/{game_id}/{market}/update", response_model=OddsQueryResponseModel)
def update_match_state(game_id: str, market: str, update: BallUpdateModel):
    try:
        odds = game_registry.grpc_client.update_match_state(game_id, update.dict())
        return OddsQueryResponseModel(winProbability=odds)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/odds/{game_id}/{market}", response_model=OddsQueryResponseModel)
def get_odds(game_id: str, market: str):
    try:
        odds = game_registry.grpc_client.get_latest_odds(game_id, market)
        return OddsQueryResponseModel(winProbability=odds)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/odds/{game_id}/{market}/init", response_model=AckResponseModel)
def set_initial_odds(game_id: str, market: str, payload: SetInitialOddsModel):
    try:
        result = game_registry.grpc_client.set_initial_odds(game_id, market, payload.initialProbability)
        return AckResponseModel(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))