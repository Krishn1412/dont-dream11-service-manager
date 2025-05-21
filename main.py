from fastapi import FastAPI, HTTPException
from api.models import (
    BetRequestModel,
    BetResponseModel,
    SetInitialOddsModel,
    OddsQueryResponseModel,
    AckResponseModel,
)
from api.models import Bet
from core.game_registry import GameRegistry
from generated.grpc_client import GRPCClient
from core.game_updater import GameUpdater

app = FastAPI()

grpc_client = GRPCClient()
game_registry = GameRegistry(grpc_client)
game_updater = GameUpdater(game_registry, grpc_client)


@app.on_event("startup")
async def startup_event():
    # If you want to start existing games from DB here, do it
    print("Game Service starting...")


@app.on_event("shutdown")
async def shutdown_event():
    await game_updater.shutdown()
    print("Game Service shut down cleanly.")


@app.post("/game/{game_id}/market/{market}/init", response_model=AckResponseModel)
async def initialize_game(game_id: str, market: str, payload: SetInitialOddsModel):
    try:
        game_registry.add_market(game_id, market, payload.initialProbability)

        grpc_client.set_initial_odds(game_id, market, payload.initialProbability)

        await game_updater.start_game_updates(game_id)

        return AckResponseModel(
            success=True, message="Game initialized and updater started."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
