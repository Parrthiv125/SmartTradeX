# smarttradex_core/strategies/strategy_router.py

from smarttradex_core.strategies.momentum import MomentumStrategy
from smarttradex_core.strategies.mean_reversion import MeanReversionStrategy
from smarttradex_core.strategies.breakout import BreakoutStrategy
from smarttradex_core.strategies.swing import SwingStrategy
from smarttradex_core.database.postgres_db import PostgresDB


# -----------------------------------
# GLOBAL SIGNAL BUFFER (API ACCESS)
# -----------------------------------

LATEST_SIGNAL = None


# -----------------------------------
# PREDICTION LOGGER
# -----------------------------------
def log_prediction(signal,
                   confidence,
                   entry_price):

    try:

        db = PostgresDB()

        conn = db.conn
        cursor = conn.cursor()

        query = """
        INSERT INTO prediction_history
        (signal, confidence, entry_price)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                signal,
                confidence,
                entry_price
            )
        )

        conn.commit()

    except Exception as e:

        print(
            "Prediction log error:",
            e
        )


# -----------------------------------
# STRATEGY ROUTER CLASS
# -----------------------------------

class StrategyRouter:

    def __init__(self):

        self.momentum = MomentumStrategy()
        self.mean_reversion = MeanReversionStrategy()
        self.breakout = BreakoutStrategy()
        self.swing = SwingStrategy()

    # -----------------------------------
    # MAIN ROUTING FUNCTION
    # -----------------------------------

    def route(self,
              prediction: dict,
              regime: str):

        global LATEST_SIGNAL

        # STRATEGY SELECTION
        if regime == "trend":
            signal = self.momentum.generate_signal(prediction)

        elif regime == "range":
            signal = self.mean_reversion.generate_signal(prediction)

        elif regime == "volatile":
            signal = self.breakout.generate_signal(prediction)

        else:
            signal = self.swing.generate_signal(prediction)

        # NORMALIZE SIGNAL
        if isinstance(signal, dict):

            sig = signal.get("signal", "HOLD")

            conf = signal.get(
                "confidence",
                prediction.get("confidence", 0.0)
            )

        elif isinstance(signal, str):

            sig = signal
            conf = prediction.get("confidence", 0.0)

        else:

            sig = "HOLD"
            conf = 0.0

        # ENTRY PRICE FROM PREDICTION
        entry_price = prediction.get(
            "price",
            0
        )

        # STORE LATEST SIGNAL
        LATEST_SIGNAL = {
            "time": int(prediction.get("time", 0)),
            "signal": sig,
            "confidence": float(conf)
        }

        # LOG TO DATABASE
        if sig in ["LONG", "SHORT"]:

            log_prediction(
                sig,
                conf,
                entry_price
            )

        print(
            "LATEST SIGNAL:",
            LATEST_SIGNAL
        )

        return signal
