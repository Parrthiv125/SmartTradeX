from fastapi import APIRouter, Request

router = APIRouter(prefix="/state", tags=["state"])


@router.get("")
def get_state(request: Request):
    engine = request.app.state.engine

    return {
        "engine_status": engine.status(),
        "running": engine.is_running(),

        # placeholders (GUI-safe)
        "market_data": {},
        "prediction": {},
        "markers": [],
        "trades": [],
        "candles": [],

        "mode": "paper",
        "symbol": "BTCUSDT",
        "timeframe": "5m"
    }
