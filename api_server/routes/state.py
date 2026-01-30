# api_server/routes/state.py


from fastapi import APIRouter, Request

router = APIRouter(prefix="/state", tags=["state"])


@router.get("")
def get_engine_state(request: Request):
    engine = request.app.state.engine
    return engine.state.snapshot()