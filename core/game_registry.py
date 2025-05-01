class GameRegistry:
    def __init__(self):
        self.games = {}

    def register_game(self, game_id):
        if game_id not in self.games:
            self.games[game_id] = {}
    
    def add_market(self, game_id, market_name, initial_odds=None):
        self.register_game(game_id)
        if market_name not in self.games[game_id]:
            self.games[game_id][market_name] = {
                "odds": initial_odds,
                "bets": [],
            }
    
    def update_odds(self, game_id, market_name, new_odds):
        if game_id in self.games and market_name in self.games[game_id]:
            self.games[game_id][market_name]["odds"] = new_odds

    def add_bet(self, game_id, market_name, bet_data):
        if game_id in self.games and market_name in self.games[game_id]:
            self.games[game_id][market_name]["bets"].append(bet_data)
    
    def get_market_info(self, game_id, market_name):
        return self.games.get(game_id, {}).get(market_name, None)
    
    def get_all_games(self):
        return self.games

    def game_exists(self, game_id):
        return game_id in self.games

    def market_exists(self, game_id, market_name):
        return self.game_exists(game_id) and market_name in self.games[game_id]