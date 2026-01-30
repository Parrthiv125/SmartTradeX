# api_server/routes/state.py


from fastapi import APIRouter, Request

router = APIRouter(prefix="/state", tags=["state"])


@router.get("")
def get_engine_state(request: Request):
    engine = request.app.state.engine

    snapshot = engine.state.snapshot()
    snapshot["candles"] = engine.candle_buffer.get_last(50)

    return snapshot
