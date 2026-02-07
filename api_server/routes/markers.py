# api_server/routes/markers.py

from fastapi import APIRouter

router = APIRouter()


@router.get("/markers")
def get_markers():
    """
    Return trading markers (BUY / SELL / HOLD).
    """
    return {
        "markers": [],
        "message": "No markers available yet"
    }
from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter(prefix="/markers", tags=["markers"])


@router.get("")
def get_markers():
    now = datetime.utcnow()

    return [
        {
            "type": "PREDICTION",
            "time": (now - timedelta(minutes=15)).isoformat(),
            "price": 30050.0,
            "confidence": 0.62
        },
        {
            "type": "BUY",
            "time": (now - timedelta(minutes=10)).isoformat(),
            "price": 29980.0,
            "confidence": 0.75
        },
        {
            "type": "SELL",
            "time": (now - timedelta(minutes=5)).isoformat(),
            "price": 30120.0,
            "confidence": 0.68
        }
    ]
