from ..generated.odds_engine_pb2 import Bet
from concurrent.futures import ThreadPoolExecutor, as_completed

class BetManager:
    
    def __init__(self, game_id: str):
        self.game_id = game_id

    def place_bet(self, market: str, bet: Bet):
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(self.validate_bet, bet): "validate",
                executor.submit(self.query_latest_odds): "odds"
            }

            latest_odds = None

            for future in as_completed(futures):
                task = futures[future]
                result = future.result()

                if task == "odds":
                    latest_odds = result

        self.active_bets.append(bet)
        self.update_exposure(bet)

        return latest_odds

    def validate_bet(self, market: str, bet: Bet):
        # Add rules: max stake, odds mismatch, etc. TODO
        pass

    def update_exposure(self, market: str, bet: Bet):
        #Call odds engine from here and update the code
        pass
    def query_latest_odds(self, market: str) -> OddsResponse:
        # gRPC call to C++ OddsEngine
        pass
