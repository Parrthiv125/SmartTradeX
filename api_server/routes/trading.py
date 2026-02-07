from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("")
def get_mock_trades():
    now = datetime.utcnow()

    return [
        {
            "id": 1,
            "symbol": "BTCUSDT",
            "side": "BUY",
            "entry_price": 29980.0,
            "exit_price": None,
            "quantity": 0.01,
            "status": "OPEN",
            "pnl": 0.0,
            "entry_time": (now - timedelta(minutes=12)).isoformat(),
            "exit_time": None
        },
        {
            "id": 2,
            "symbol": "BTCUSDT",
            "side": "SELL",
            "entry_price": 30050.0,
            "exit_price": 29980.0,
            "quantity": 0.01,
            "status": "CLOSED",
            "pnl": 0.7,
            "entry_time": (now - timedelta(minutes=25)).isoformat(),
            "exit_time": (now - timedelta(minutes=5)).isoformat()
        }
    ]
