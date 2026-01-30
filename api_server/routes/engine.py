# api_server/routes/engine.py

from fastapi import APIRouter

router = APIRouter()

@router.post("/engine/start")
def start_engine():
    """
    Start the trading engine.
    Actual engine logic is handled elsewhere.
    """
    return {
        "action": "start",
        "status": "accepted",
        "message": "Engine start requested"
    }


@router.post("/engine/stop")
def stop_engine():
    """
    Stop the trading engine.
    """
    return {
        "action": "stop",
        "status": "accepted",
        "message": "Engine stop requested"
    }


@router.post("/engine/reset")
def reset_engine():
    """
    Reset the trading engine state.
    """
    return {
        "action": "reset",
        "status": "accepted",
        "message": "Engine reset requested"
    }
