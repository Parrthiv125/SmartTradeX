from fastapi import APIRouter

from smarttradex_core.database.postgres_db import PostgresDB
from smarttradex_core.analytics.trade_analytics import TradeAnalytics
from smarttradex_core.analytics.accuracy_tracker import AccuracyTracker


router = APIRouter(prefix="/analytics", tags=["Analytics"])


db = PostgresDB()
analytics = TradeAnalytics()
accuracy_tracker = AccuracyTracker()


# --------------------------------------------------
# PAPER TRADES
# --------------------------------------------------
@router.get("/paper_trades")
def get_paper_trades():

    trades = db.fetch_all_trades()

    return {
        "count": len(trades),
        "trades": trades
    }


# --------------------------------------------------
# PERFORMANCE METRICS
# --------------------------------------------------
@router.get("/performance_metrics")
def performance_metrics():

    return analytics.summary()


# --------------------------------------------------
# ACCURACY METRICS
# --------------------------------------------------
@router.get("/accuracy")
def accuracy_metrics():

    return accuracy_tracker.summary()
