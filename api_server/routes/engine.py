from fastapi import APIRouter, Request

router = APIRouter(prefix="/engine", tags=["engine"])


@router.post("/start")
def start_engine(request: Request):
    runtime = request.app.state.runtime
    runtime.start()

    return {
        "action": "start",
        "status": "ok",
        "message": "Engine start requested (mock)"
    }


@router.post("/stop")
def stop_engine(request: Request):
    runtime = request.app.state.runtime
    runtime.stop()

    return {
        "action": "stop",
        "status": "ok",
        "message": "Engine stop requested (mock)"
    }
