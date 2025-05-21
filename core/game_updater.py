import threading
import time
import requests
from generated.odds_engine_pb2 import BallUpdate, MatchStateRequest
from typing import Dict


class GameUpdater:
    def __init__(self, grpc_client, interval=5):
        self.grpc_client = grpc_client
        self.interval = interval
        self.polling_threads: Dict[str, threading.Thread] = {}
        self.running_flags: Dict[str, bool] = {}

    def start_polling(self, game_id):
        if game_id in self.polling_threads:
            return

        self.running_flags[game_id] = True

        def poll():
            while self.running_flags[game_id]:
                try:
                    response = requests.get(
                        f"http://localhost:8000/game/{game_id}/latest"
                    )
                    if response.status_code == 200:
                        data = response.json()
                        ball_update = BallUpdate(**data)
                        request = MatchStateRequest(gameId=game_id, update=ball_update)
                        self.grpc_client.stub.UpdateMatchState(request)
                        print(f"[Updater] Sent update for {game_id}: {data}")
                except Exception as e:
                    print(f"[Updater] Error polling for {game_id}: {e}")
                time.sleep(self.interval)

        thread = threading.Thread(target=poll, daemon=True)
        self.polling_threads[game_id] = thread
        thread.start()

    def stop_polling(self, game_id):
        self.running_flags[game_id] = False
