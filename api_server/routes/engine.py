# api_server/routes/engine.py

from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/engine/start")
def start_engine(request: Request):
    runtime = request.app.state.runtime
    runtime.start()
    return {
        "action": "start",
        "status": "ok",
        "message": "Engine runtime started"
    }

@router.post("/engine/stop")
def stop_engine(request: Request):
    runtime = request.app.state.runtime
    runtime.stop()
    return {
        "action": "stop",
        "status": "ok",
        "message": "Engine runtime stopped"
    }

@router.post("/engine/reset")
def reset_engine(request: Request):
    engine = request.app.state.engine
    engine.reset()
    return {
        "action": "reset",
        "status": "ok",
        "message": "Engine state reset"
    }
