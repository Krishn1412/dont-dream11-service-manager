# dont-dream11-service-manager
# Dont-dream11 Odds Service Manager

This is a FastAPI-based backend service that acts as the **entry point** between a frontend or external APIs and a high-performance C++ **odds engine**. It handles:

- Game initialization
- Match state polling and updates
- Bet placement
- Odds queries
- Communication with the C++ gRPC odds engine

It integrates with a mock API for ball-by-ball cricket match updates.

---

## Features

- **Game & Market Registration**
- **Bet Management** (stake, market, team, etc.)
- **Odds Querying** (calls gRPC backend)
- **Real-Time Match State Updates** (polling mock data)
- **gRPC Integration** with C++ odds engine
- FastAPI-powered web server

---

## How It Works

### 🏁 Game Initialization
- Registers a game and market in the `GameRegistry`.
- Sets initial odds via gRPC.
- Starts a background polling thread for mock match updates.

### 🔄 Polling
- A background thread (`GameUpdater`) fetches simulated ball-by-ball updates.
- Each update is streamed to the gRPC-based C++ Odds Engine.

### 💸 Bet Placement
- Validates incoming bet requests.
- Updates exposure and market state in memory.
- Sends bet details to the gRPC Odds Engine.
- Tracks bet locally for settlement or auditing.

### 📈 Odds Updates
- Odds are not cached — always fetched live from the Odds Engine via gRPC.
- Reflect current match state and exposure instantly.

---


## 🧠 Project Structure

```bash
.
├── main.py                  # FastAPI app entry point
├── core/
│   ├── bet_manager.py       # Manages bet placement and exposure tracking
│   ├── game_registry.py     # Tracks games and markets
│   └── game_updater.py      # Polls for match updates and pushes them via gRPC
├── proto/
│   ├── odds_engine_pb2.py   # gRPC message definitions
│   └── grpc_client.py       # gRPC client wrapper for odds engine
├── api/
│   └── models.py            # Pydantic models for request/response bodies
├── mock_api.py              # Simulates real-time cricket match data
├── tests/                   # Unit tests
└── README.md
```

##  Getting Started

### Prerequisites

- Python 3.8+
- gRPC-compatible Odds Engine (C++ backend)
- `venv` (Python virtual environment)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/service-manager.git
cd service-manager

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```
### Running the tests
```bash
 python -m pytest tests/test_main.py
```
### Starting the server

```bash
python main.py
```
This is the main server that communicates with api calls and calls the odds engine.This runs at http://localhost:8000.
```bash
python utils/mock_api.py
```
## 📬 API Usage Examples

### ➕ Initialize a Game
```bash
http POST localhost:8000/game/match123/market/match_winner/init initialProbability:=0.6
```

### ➕ Place a Bet
```bash
http POST localhost:8000/bet/match123/match_winner \
  userId="user1" stake:=100 odds:=1.5 market="match_winner" teamA:=true
```

### ➕ Get Current Odds
```bash
http GET localhost:8000/odds/match123/match_winner
```

### ➕ Stop Polling for a Game
```bash
http POST localhost:8000/game/match123/stop
```
