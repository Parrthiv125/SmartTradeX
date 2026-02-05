from fastapi import APIRouter, Request

router = APIRouter(prefix="/state", tags=["state"])


@router.get("")
def get_engine_state(request: Request):
    """
    TEMPORARY SAFE STATE ENDPOINT (Validation Mode)

    Purpose:
    Prevent API crashes caused by non-JSON-safe objects
    during live trading validation.
    """

    engine = request.app.state.engine
    state = engine.state

    return {
        "market_data": state.market_data or {},
        "prediction": state.prediction or {},

        # LIMIT markers (last 20 only)
        "markers": state.markers[-20:] if state.markers else [],

        # LIMIT trades (last 20 only)
        "trades": state.trades[-20:] if state.trades else [],

        "features": getattr(state, "features", {}),

        # LIMIT candles
        "candles": engine.candle_buffer.get_last(30),

        "running": engine.running
    }
