from pydantic import BaseModel
from typing import Dict, List


class Bet(BaseModel):
    userId: str
    stake: float
    odds: float
    market: str
    teamA: bool


class BetRequestModel(BaseModel):
    userId: str
    stake: float
    odds: float
    market: str
    teamA: bool


class BetResponseModel(BaseModel):
    winProbability: float
    exposure: Dict[str, float]


class BallUpdateModel(BaseModel):
    innings: int
    targetScore: int
    currentScore: int
    wicketsLeft: int
    ballsRemaining: int
    recentRuns: List[int]
    striker: str
    nonStriker: str
    pitchModifier: float
    isWicket: bool
    isDot: bool
    isExtra: bool
    isBoundary: bool
    bowler: str
    runs: int


class MatchStateRequestModel(BaseModel):
    gameId: str
    update: BallUpdateModel


class SetInitialOddsModel(BaseModel):
    initialProbability: float


class OddsQueryResponseModel(BaseModel):
    winProbability: float


class AckResponseModel(BaseModel):
    success: bool
    message: str
