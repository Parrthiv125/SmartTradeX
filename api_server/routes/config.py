# api_server/routes/config.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/engine/config")
def engine_config():
    """
    Static engine configuration (temporary).
    """
    return {
        "symbol": "BTCUSDT",
        "timeframe": "1m",
        "mode": "paper",
        "status": "config loaded"
    }
