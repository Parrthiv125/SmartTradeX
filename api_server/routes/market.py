from fastapi import APIRouter, Query

from smarttradex_core.data.binance_client import BinanceClient
from smarttradex_core.streaming.candle_stream import (
    get_live_candles,
    start_candle_stream
)

router = APIRouter(prefix="/market", tags=["market"])

client = BinanceClient()

# Start websocket stream once when router loads
start_candle_stream()


# ---------------------------------------------
# Historical candles (REST)
# ---------------------------------------------
@router.get("/candles")
def get_market_candles(interval: str = Query("5m")):
    candles = client.get_candles(
        symbol="BTCUSDT",
        interval=interval,
        limit=200
    )

    return {
        "symbol": "BTCUSDT",
        "timeframe": interval,
        "candles": candles
    }


# ---------------------------------------------
# LIVE candles (WebSocket buffer)
# ---------------------------------------------
@router.get("/live_candles")
def live_candles():
    return {
        "symbol": "BTCUSDT",
        "candles": get_live_candles()
    }
