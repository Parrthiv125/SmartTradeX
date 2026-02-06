import time
from smarttradex_core.trading.position_sizer import PositionSizer


class PaperBroker:
    """
    Simulates paper trading with basic risk management.
    Keeps full trade history.
    Supports ONE open position at a time.
    """

    def __init__(self):

        # ─────────────────────────────
        # Capital & Position Sizing
        # ─────────────────────────────
        self.capital = 10000  # Default paper capital
        self.position_sizer = PositionSizer(self.capital, 0.02)

        # Confidence thresholds
        self.entry_confidence_threshold = 0.60
        self.exit_confidence_threshold = 0.45

        self.position = None
        self.trades = []  # Closed trades history

        # ─────────────────────────────
        # Risk Parameters
        # ─────────────────────────────
        self.stop_loss_pct = -0.01     # -1%
        self.take_profit_pct = 0.02    # +2%
        self.max_hold_seconds = 300    # 5 minutes

    # ─────────────────────────────────────────────
    # PROCESS MARKERS
    # ─────────────────────────────────────────────
    def process_marker(self, marker: dict, price: float):
        """
        Process a marker and decide trade actions.
        Returns trade dict if a trade is closed.
        """

        current_time = time.time()

        action = marker.get("action")
        confidence = marker.get("confidence", 0.0)

        # =========================================================
        # NO OPEN POSITION → ENTRY LOGIC
        # =========================================================
        if self.position is None:

            # Confidence gate for entry
            if (
                action == "BUY"
                and confidence >= self.entry_confidence_threshold
            ):

                qty = self.position_sizer.calculate_position_size(price)

                self.position = {
                    "side": "LONG",
                    "entry_price": float(price),
                    "qty": float(qty),
                    "entry_time": float(current_time),
                    "status": "OPEN",
                    "entry_confidence": float(confidence)
                }

            return None

        # =========================================================
        # OPEN POSITION → EXIT LOGIC
        # =========================================================
        entry_price = self.position["entry_price"]
        entry_time = self.position["entry_time"]
        qty = self.position["qty"]

        pnl_pct = (price - entry_price) / entry_price
        pnl_value = pnl_pct * (qty * entry_price)

        held_seconds = current_time - entry_time

        exit_reason = None

        # ───────────── Risk exits ─────────────
        if pnl_pct <= self.stop_loss_pct:
            exit_reason = "STOP_LOSS"

        elif pnl_pct >= self.take_profit_pct:
            exit_reason = "TAKE_PROFIT"

        elif held_seconds >= self.max_hold_seconds:
            exit_reason = "TIME_EXIT"

        elif action == "SELL":
            exit_reason = "SIGNAL_EXIT"

        # ───────────── Confidence decay exit ─────────────
        elif confidence < self.exit_confidence_threshold:
            exit_reason = "CONFIDENCE_DROP"

        # =========================================================
        # CLOSE TRADE
        # =========================================================
        if exit_reason:

            trade = {
                "side": "LONG",

                # Prices
                "entry_price": float(entry_price),
                "exit_price": float(price),

                # Quantity
                "qty": float(qty),

                # Time fields
                "entry_time": float(entry_time),
                "exit_time": float(current_time),
                "timestamp": float(current_time),

                # Performance
                "pnl_pct": float(round(pnl_pct, 4)),
                "pnl_value": float(round(pnl_value, 2)),
                "hold_seconds": int(held_seconds),

                # Metadata
                "reason": exit_reason,
                "entry_confidence": self.position.get("entry_confidence")
            }

            # Store trade
            self.trades.append(trade)

            # Update capital
            self.capital += pnl_value
            self.position_sizer.update_capital(self.capital)

            # Reset position
            self.position = None

            return trade

        return None

    # ─────────────────────────────────────────────
    # HISTORY ACCESS
    # ─────────────────────────────────────────────
    def get_trade_history(self):
        """Return all closed trades."""
        return self.trades
