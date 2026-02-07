from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/candles")
def get_mock_candles():
    candles = []
    now = datetime.utcnow()
    price = 30000.0

    for i in range(30):
        open_p = price
        close_p = open_p + random.uniform(-50, 50)
        high_p = max(open_p, close_p) + random.uniform(0, 30)
        low_p = min(open_p, close_p) - random.uniform(0, 30)

        candles.append({
            "time": (now - timedelta(minutes=5 * (30 - i))).isoformat(),
            "open": round(open_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "close": round(close_p, 2),
            "volume": round(random.uniform(10, 100), 2)
        })

        price = close_p

    return {
        "symbol": "BTCUSDT",
        "timeframe": "5m",
        "candles": candles
    }
