import time
from datetime import datetime

from smarttradex_core.trading.position_sizer import PositionSizer
from smarttradex_core.database.postgres_db import PostgresDB


class PaperBroker:
    """
    Simulates paper trading with risk management.
    Stores trades in Supabase PostgreSQL.
    """

    def __init__(self):

        # ─────────────────────────────
        # Capital & Position Sizing
        # ─────────────────────────────
        self.capital = 10000
        self.position_sizer = PositionSizer(self.capital, 0.02)

        # ─────────────────────────────
        # Confidence Filters
        # ─────────────────────────────
        self.entry_confidence_threshold = 0.60
        self.exit_confidence_threshold = 0.45

        # ─────────────────────────────
        # Cooldown Control
        # ─────────────────────────────
        self.trade_cooldown_seconds = 60
        self.last_trade_time = 0

        # ─────────────────────────────
        # Position + History
        # ─────────────────────────────
        self.position = None
        self.trades = []

        # ─────────────────────────────
        # Risk Parameters
        # ─────────────────────────────
        self.stop_loss_pct = -0.01
        self.take_profit_pct = 0.02
        self.max_hold_seconds = 300

        # ─────────────────────────────
        # DATABASE CONNECTION
        # ─────────────────────────────
        self.db = PostgresDB()
        self.current_trade_id = None

    # ─────────────────────────────────────────────
    # PROCESS MARKERS
    # ─────────────────────────────────────────────
    def process_marker(self, marker: dict, price: float):

        current_time = time.time()

        action = marker.get("action")
        confidence = marker.get("confidence", 0.0)

        # =========================================================
        # ENTRY LOGIC
        # =========================================================
        if self.position is None:

            time_since_last_trade = (
                current_time - self.last_trade_time
            )

            if time_since_last_trade < self.trade_cooldown_seconds:
                return None

            if (
                action == "BUY"
                and confidence >= self.entry_confidence_threshold
            ):

                qty = self.position_sizer.calculate_position_size(
                    price
                )

                self.position = {
                    "side": "LONG",
                    "entry_price": float(price),
                    "qty": float(qty),
                    "entry_time": float(current_time),
                    "status": "OPEN",
                    "entry_confidence": float(confidence)
                }

                # ───────── DB INSERT ─────────
                self.db.insert_trade(
                    entry_time=datetime.now(),
                    side="LONG",
                    entry_price=price,
                    quantity=qty,
                    confidence=confidence,
                    strategy="Momentum"
                )

                self.current_trade_id = (
                    self.db.get_last_open_trade()
                )

            return None

        # =========================================================
        # EXIT LOGIC
        # =========================================================
        entry_price = self.position["entry_price"]
        entry_time = self.position["entry_time"]
        qty = self.position["qty"]

        pnl_pct = (price - entry_price) / entry_price
        pnl_value = pnl_pct * (qty * entry_price)

        held_seconds = current_time - entry_time

        exit_reason = None

        if pnl_pct <= self.stop_loss_pct:
            exit_reason = "STOP_LOSS"

        elif pnl_pct >= self.take_profit_pct:
            exit_reason = "TAKE_PROFIT"

        elif held_seconds >= self.max_hold_seconds:
            exit_reason = "TIME_EXIT"

        elif action == "SELL":
            exit_reason = "SIGNAL_EXIT"

        elif confidence < self.exit_confidence_threshold:
            exit_reason = "CONFIDENCE_DROP"

        # =========================================================
        # CLOSE TRADE
        # =========================================================
        if exit_reason:

            trade = {
                "side": "LONG",
                "entry_price": float(entry_price),
                "exit_price": float(price),
                "qty": float(qty),
                "entry_time": float(entry_time),
                "exit_time": float(current_time),
                "timestamp": float(current_time),
                "pnl_pct": float(round(pnl_pct, 4)),
                "pnl_value": float(round(pnl_value, 2)),
                "hold_seconds": int(held_seconds),
                "reason": exit_reason,
                "entry_confidence": self.position.get(
                    "entry_confidence"
                )
            }

            # ───────── DB UPDATE ─────────
            self.db.close_trade(
                trade_id=self.current_trade_id,
                exit_time=datetime.now(),
                exit_price=price,
                pnl_pct=pnl_pct * 100,
                pnl_value=pnl_value
            )

            self.trades.append(trade)

            self.capital += pnl_value
            self.position_sizer.update_capital(self.capital)

            self.last_trade_time = current_time
            self.position = None
            self.current_trade_id = None

            return trade

        return None

    # ─────────────────────────────────────────────
    # HISTORY ACCESS
    # ─────────────────────────────────────────────
    def get_trade_history(self):
        return self.trades
