from fastapi import APIRouter
import smarttradex_core.strategies.strategy_router as router_module
from smarttradex_core.database.postgres_db import PostgresDB


router = APIRouter(prefix="/predictions")


@router.get("/latest")
def latest_prediction():

    try:
        latest_signal = router_module.LATEST_SIGNAL

        if latest_signal is None:
            return {
                "signal": "HOLD",
                "confidence": 0
            }

        return latest_signal

    except Exception as e:
        return {
            "error": str(e)
        }

# =========================================
# PREDICTION HISTORY API
# =========================================
@router.get("/history")
def prediction_history():

    try:

        db = PostgresDB()

        conn = db.conn
        cursor = conn.cursor()

        query = """
        SELECT
          time,
          signal,
          confidence,
          outcome,
          pnl_pct
        FROM prediction_history
        ORDER BY time DESC
        LIMIT 20
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        history = []

        for row in rows:

            history.append({
                "time": row[0],
                "signal": row[1],
                "confidence": row[2],
                "outcome": row[3],
                "pnl_pct": row[4]
            })

        return {
            "count": len(history),
            "history": history
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# =========================================
# PREDICTION ANALYTICS
# =========================================
@router.get("/analytics")
def prediction_analytics():

    try:

        db = PostgresDB()
        conn = db.conn
        cursor = conn.cursor()

        # TOTAL SIGNALS
        cursor.execute("""
            SELECT COUNT(*)
            FROM prediction_history
        """)
        total = cursor.fetchone()[0]

        # WON SIGNALS
        cursor.execute("""
            SELECT COUNT(*)
            FROM prediction_history
            WHERE outcome = 'WON'
        """)
        wins = cursor.fetchone()[0]

        accuracy = (
            (wins / total) * 100
            if total > 0 else 0
        )

        # AVG RISK / REWARD (mock until trade link)
        cursor.execute("""
            SELECT AVG(pnl_pct)
            FROM prediction_history
            WHERE outcome != 'OPEN'
        """)
        avg_rr = cursor.fetchone()[0] or 0

        return {
            "total_predictions": total,
            "accuracy": accuracy,
            "avg_rr": avg_rr
        }

    except Exception as e:

        return {
            "error": str(e)
        }
