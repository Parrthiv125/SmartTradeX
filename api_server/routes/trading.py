# api_server/routes/trading.py

from fastapi import APIRouter

router = APIRouter()


@router.get("/trading/positions")
def get_positions():
    """
    Return current paper trading positions.
    """
    return {
        "positions": [],
        "message": "No open positions"
    }


@router.get("/trading/trades")
def get_trades():
    """
    Return paper trade history.
    """
    return {
        "trades": [],
        "message": "No trades executed yet"
    }


@router.get("/trading/pnl")
def get_pnl():
    """
    Return current paper trading PnL.
    """
    return {
        "pnl": {
            "realized": 0.0,
            "unrealized": 0.0,
            "total": 0.0
        }
    }
