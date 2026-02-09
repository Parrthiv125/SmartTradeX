from fastapi import APIRouter, Query
from smarttradex_core.data.binance_client import BinanceClient

router = APIRouter(prefix="/market", tags=["market"])

client = BinanceClient()


@router.get("/candles")
def get_market_candles(interval: str = Query("5m")):
    """
    Return REAL Binance OHLCV candles
    """

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
