from fastapi import APIRouter

from smarttradex_core.database.postgres_db import PostgresDB
from smarttradex_core.analytics.trade_analytics import TradeAnalytics
from smarttradex_core.analytics.accuracy_tracker import AccuracyTracker


router = APIRouter(prefix="/analytics", tags=["Analytics"])


db = PostgresDB()
analytics = TradeAnalytics()
accuracy_tracker = AccuracyTracker()


# --------------------------------------------------
# PAPER TRADES (ALL)
# --------------------------------------------------
@router.get("/paper_trades")
def get_paper_trades():

    trades = db.fetch_all_trades()

    return {
        "count": len(trades),
        "trades": trades
    }


# --------------------------------------------------
# OPEN TRADES (NEW - PHASE 10 REAL)
# --------------------------------------------------
@router.get("/trades/open")
def get_open_trades():

    all_trades = db.fetch_all_trades()

    open_trades = []

    for trade in all_trades:

        # Your trade array structure:
        # [id, entry_time, exit_time, side, entry_price, exit_price,
        #  qty, pnl_pct, pnl_value, confidence, strategy, status, created_at]

        if trade[11] == "OPEN":   # status column

            open_trades.append({
                "trade_id": trade[0],
                "entry_time": trade[1],
                "side": trade[3],
                "entry_price": trade[4],
                "quantity": trade[6],
                "confidence": trade[9],
                "strategy": trade[10],
                "status": trade[11]
            })

    return {
        "count": len(open_trades),
        "trades": open_trades
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

# =========================================
# PORTFOLIO ANALYTICS (FINAL)
# =========================================
@router.get("/portfolio/summary")
def portfolio_summary():

    try:

        db = PostgresDB()
        conn = db.conn
        cursor = conn.cursor()

        # TOTAL TRADES
        cursor.execute("""
            SELECT COUNT(*)
            FROM paper_trades
            WHERE status = 'CLOSED'
        """)
        total_trades = cursor.fetchone()[0]

        # WINNING TRADES
        cursor.execute("""
            SELECT COUNT(*)
            FROM paper_trades
            WHERE pnl_value > 0
            AND status = 'CLOSED'
        """)
        wins = cursor.fetchone()[0]

        # LOSING TRADES
        cursor.execute("""
            SELECT COUNT(*)
            FROM paper_trades
            WHERE pnl_value < 0
            AND status = 'CLOSED'
        """)
        losses = cursor.fetchone()[0]

        # WIN RATE
        win_rate = (
            (wins / total_trades) * 100
            if total_trades > 0 else 0
        )

        # TOTAL PROFIT
        cursor.execute("""
            SELECT SUM(pnl_value)
            FROM paper_trades
            WHERE status = 'CLOSED'
        """)
        total_profit = cursor.fetchone()[0] or 0

        # AVG WIN
        cursor.execute("""
            SELECT AVG(pnl_value)
            FROM paper_trades
            WHERE pnl_value > 0
            AND status = 'CLOSED'
        """)
        avg_win = cursor.fetchone()[0] or 0

        # AVG LOSS
        cursor.execute("""
            SELECT AVG(pnl_value)
            FROM paper_trades
            WHERE pnl_value < 0
            AND status = 'CLOSED'
        """)
        avg_loss = cursor.fetchone()[0] or 0

        # PROFIT FACTOR
        profit_factor = (
            abs(avg_win / avg_loss)
            if avg_loss != 0 else 0
        )

        return {

            "total_trades": total_trades,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "total_profit": total_profit,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "profit_factor": profit_factor
        }

    except Exception as e:

        return {"error": str(e)}
    
# =========================================
# RECENT TRADE ACTIVITY
# =========================================
@router.get("/portfolio/recent-activity")
def recent_activity():

    try:

        db = PostgresDB()
        conn = db.conn
        cursor = conn.cursor()

        query = """
        SELECT
          side,
          status,
          entry_price,
          pnl_value,
          entry_time,
          exit_time
        FROM paper_trades
        ORDER BY created_at DESC
        LIMIT 5
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        activity = []

        for row in rows:

            side = row[0]
            status = row[1]

            if status == "OPEN":
                action = "Opened " + side
                value  = row[2]
                time   = row[4]
            else:
                action = "Closed " + side
                value  = row[3]
                time   = row[5]

            activity.append({
                "action": action,
                "value": value or 0,
                "time": time,
                "status": status
            })

        return {"activity": activity}

    except Exception as e:

        return {"error": str(e)}

