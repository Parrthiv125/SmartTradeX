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
