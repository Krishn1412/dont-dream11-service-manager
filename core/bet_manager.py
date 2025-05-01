class BetManager:
    
    def __init__(self, game_id: str, market: str):
        self.game_id = game_id
        self.market = market
        self.active_bets = []  # List[Bet]
        self.exposure = {"teamA": 0.0, "teamB": 0.0}

    def place_bet(self, bet: Bet):
        self.validate_bet(bet)
        self.active_bets.append(bet)
        self.update_exposure(bet)
        return self.query_latest_odds()

    def validate_bet(self, bet: Bet):
        # Add rules: max stake, odds mismatch, etc.
        pass

    def update_exposure(self, bet: Bet):
        if bet.teamA:
            self.exposure["teamA"] += bet.stake
        else:
            self.exposure["teamB"] += bet.stake

    def query_latest_odds(self) -> OddsResponse:
        # gRPC call to C++ OddsEngine
        pass
