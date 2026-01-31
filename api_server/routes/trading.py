from fastapi import APIRouter, Request

router = APIRouter(prefix="/trading", tags=["trading"])


@router.get("/trades")
def get_trades(request: Request):
    """
    Return paper trade history.
    """
    engine = request.app.state.engine
    return {
        "trades": engine.state.trades
    }
