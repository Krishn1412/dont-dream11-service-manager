from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from api.models import (
    BetRequestModel,
    BetResponseModel,
    SetInitialOddsModel,
    OddsQueryResponseModel,
    AckResponseModel,
    Bet,
)
from core.game_registry import GameRegistry
from proto.grpc_client import GRPCClient
from core.game_updater import GameUpdater


grpc_client = GRPCClient()
game_updater = GameUpdater(grpc_client)
game_registry = GameRegistry(grpc_client, game_updater)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Game Service starting...")
    yield  # No shutdown logic needed since polling threads are daemonic
    print("Game Service shut down cleanly.")


app = FastAPI(lifespan=lifespan)


@app.post("/game/{game_id}/market/{market}/init", response_model=AckResponseModel)
async def initialize_game(game_id: str, market: str, payload: SetInitialOddsModel):
    try:
        game_registry.add_market(game_id, market, payload.initialProbability)
        grpc_client.set_initial_odds(game_id, market, payload.initialProbability)
        game_updater.start_polling(game_id)
        return AckResponseModel(success=True, message="Game initialized and updater started.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/bet/{game_id}/{market}", response_model=BetResponseModel)
def place_bet(game_id: str, market: str, bet_request: BetRequestModel):
    try:
        
        bet_manager = game_registry.get_bet_manager(game_id, market)

        bet = Bet(
            userId=bet_request.userId,
            stake=bet_request.stake,
            odds=bet_request.odds,
            market=bet_request.market,
            teamA=bet_request.teamA,
        )
        
        updated_odds = bet_manager.place_bet(bet)
        game_registry.add_bet(game_id, market, bet)
        # print(bet_manager.exposure)
        return BetResponseModel(
            winProbability=updated_odds)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/odds/{game_id}/{market}", response_model=OddsQueryResponseModel)
def get_latest_odds(game_id: str, market: str):
    try:
        print("I am here buddy")
        odds = grpc_client.get_latest_odds(game_id, market)
        return OddsQueryResponseModel(winProbability=odds.winProbability)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/game/{game_id}/stop", response_model=AckResponseModel)
def stop_polling(game_id: str):
    try:
        game_updater.stop_polling(game_id)
        return AckResponseModel(success=True, message=f"Polling stopped for game {game_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
