from fastapi import FastAPI
from fastapi.responses import JSONResponse
import random

app = FastAPI()

@app.get("/game/{game_id}/latest")
def get_latest_ball_update(game_id: str):
    return JSONResponse(
        {
            "innings": 1,
            "targetScore": 150,
            "currentScore": random.randint(0, 150),
            "wicketsLeft": random.randint(0, 10),
            "ballsRemaining": random.randint(0, 120),
            "recentRuns": [random.randint(0, 6) for _ in range(6)],
            "striker": "Player A",
            "nonStriker": "Player B",
            "pitchModifier": round(random.uniform(0.8, 1.2), 2),
            "isWicket": random.choice([False, False, True]),
            "isDot": random.choice([False, False, True]),
            "isExtra": random.choice([False, True]),
            "isBoundary": random.choice([False, True]),
            "bowler": "Bowler X",
            "runs": random.randint(0, 6),
        }
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("mock_api:app", host="0.0.0.0", port=8001, reload=True)
