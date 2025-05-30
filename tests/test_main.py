import pytest
from unittest.mock import MagicMock, patch
from main import (
    place_bet,
    get_latest_odds,
    stop_polling,
)
from api.models import BetRequestModel, SetInitialOddsModel


@pytest.fixture
def mock_dependencies():
    with patch("main.grpc_client") as mock_grpc, \
         patch("main.game_updater") as mock_updater, \
         patch("main.game_registry") as mock_registry:
        yield mock_grpc, mock_updater, mock_registry


def test_place_bet(mock_dependencies):
    mock_grpc, mock_updater, mock_registry = mock_dependencies

    fake_bet_manager = MagicMock()
    fake_bet_manager.place_bet.return_value = 0.78
    mock_registry.get_bet_manager.return_value = fake_bet_manager

    game_id = "game123"
    market = "winner"
    bet_request = BetRequestModel(
        userId="user42",
        stake=100,
        odds=1.5,
        market=market,
        teamA=True
    )

    result = place_bet(game_id, market, bet_request)

    assert result.winProbability == 0.78
    mock_registry.get_bet_manager.assert_called_once_with(game_id, market)
    fake_bet_manager.place_bet.assert_called_once()
    mock_registry.add_bet.assert_called_once()


def test_get_latest_odds(mock_dependencies):
    mock_grpc, *_ = mock_dependencies

    mock_grpc.get_latest_odds.return_value.winProbability = 0.55

    result = get_latest_odds("game123", "winner")

    assert result.winProbability == 0.55
    mock_grpc.get_latest_odds.assert_called_once_with("game123", "winner")


def test_stop_polling(mock_dependencies):
    _, mock_updater, _ = mock_dependencies

    result = stop_polling("game123")

    assert result.success is True
    assert result.message == "Polling stopped for game game123"
    mock_updater.stop_polling.assert_called_once_with("game123")
