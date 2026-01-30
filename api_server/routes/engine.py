# api_server/routes/engine.py

from fastapi import APIRouter, Request
import threading

router = APIRouter(prefix="/engine", tags=["engine"])

# single background thread reference
_runtime_thread = None


@router.post("/start")
def start_engine(request: Request):
    global _runtime_thread

    runtime = request.app.state.runtime

    # prevent duplicate starts
    if runtime.running:
        return {
            "action": "start",
            "status": "ok",
            "message": "Engine already running"
        }

    runtime.start()

    # start runtime loop in background thread
    _runtime_thread = threading.Thread(
        target=runtime.run_loop,
        args=(1.0,),   # 1 second interval
        daemon=True
    )
    _runtime_thread.start()

    return {
        "action": "start",
        "status": "ok",
        "message": "Engine runtime started"
    }


@router.post("/stop")
def stop_engine(request: Request):
    runtime = request.app.state.runtime
    runtime.stop()

    return {
        "action": "stop",
        "status": "ok",
        "message": "Engine runtime stopped"
    }


@router.post("/reset")
def reset_engine(request: Request):
    engine = request.app.state.engine
    engine.reset()

    return {
        "action": "reset",
        "status": "ok",
        "message": "Engine state reset"
    }
