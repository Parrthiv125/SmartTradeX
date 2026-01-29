# api_server/routes/state.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/engine/status")
def engine_status():
    """
    Temporary static endpoint.
    Later this will return real engine state.
    """
    return {
        "engine": "offline",
        "message": "Engine not connected yet"
    }