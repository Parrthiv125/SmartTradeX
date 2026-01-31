import time


class PaperBroker:
    """
    Simulates paper trading with basic risk management.
    Supports ONE open position at a time.
    """

    def __init__(self):
        self.position = None

        # Risk parameters
        self.stop_loss_pct = -0.01     # -1%
        self.take_profit_pct = 0.02    # +2%
        self.max_hold_seconds = 300    # 5 minutes

    def process_marker(self, marker: dict, price: float):
        """
        Process a marker and decide trade actions.
        Returns trade dict if a trade is closed.
        """

        current_time = time.time()

        # ─────────────────────────────────────────────
        # NO OPEN POSITION → check for entry
        # ─────────────────────────────────────────────
        if self.position is None:
            if marker["action"] == "BUY":
                self.position = {
                    "side": "LONG",
                    "entry_price": price,
                    "entry_time": current_time,
                    "status": "OPEN"
                }
            return None

        # ─────────────────────────────────────────────
        # OPEN POSITION → check for exit
        # ─────────────────────────────────────────────
        entry_price = self.position["entry_price"]
        entry_time = self.position["entry_time"]

        pnl_pct = (price - entry_price) / entry_price
        held_seconds = current_time - entry_time

        exit_reason = None

        if pnl_pct <= self.stop_loss_pct:
            exit_reason = "STOP_LOSS"

        elif pnl_pct >= self.take_profit_pct:
            exit_reason = "TAKE_PROFIT"

        elif held_seconds >= self.max_hold_seconds:
            exit_reason = "TIME_EXIT"

        elif marker["action"] == "SELL":
            exit_reason = "SIGNAL_EXIT"

        if exit_reason:
            trade = {
                "side": "LONG",
                "entry_price": entry_price,
                "exit_price": price,
                "pnl_pct": round(pnl_pct, 4),
                "hold_seconds": int(held_seconds),
                "reason": exit_reason
            }
            self.position = None
            return trade

        return None
