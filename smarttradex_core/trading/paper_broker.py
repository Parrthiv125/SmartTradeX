class PaperBroker:
    """
    Simulates paper trading with basic risk management.
    Supports ONE open position at a time.
    """

    def __init__(self):
        self.position = None  # None or dict

        # Risk parameters (simple & fixed)
        self.stop_loss_pct = -0.01    # -1%
        self.take_profit_pct = 0.02   # +2%

    def process_marker(self, marker: dict, price: float):
        """
        Process a marker and decide trade actions.
        Returns trade dict if a trade is closed.
        """

        # ─────────────────────────────────────────────
        # NO OPEN POSITION → check for entry
        # ─────────────────────────────────────────────
        if self.position is None:
            if marker["action"] == "BUY":
                self.position = {
                    "side": "LONG",
                    "entry_price": price,
                    "status": "OPEN"
                }
            return None

        # ─────────────────────────────────────────────
        # OPEN POSITION → check for exit
        # ─────────────────────────────────────────────
        entry_price = self.position["entry_price"]
        pnl_pct = (price - entry_price) / entry_price

        exit_reason = None

        if pnl_pct <= self.stop_loss_pct:
            exit_reason = "STOP_LOSS"

        elif pnl_pct >= self.take_profit_pct:
            exit_reason = "TAKE_PROFIT"

        elif marker["action"] == "SELL":
            exit_reason = "SIGNAL_EXIT"

        if exit_reason:
            trade = {
                "side": "LONG",
                "entry_price": entry_price,
                "exit_price": price,
                "pnl_pct": round(pnl_pct, 4),
                "reason": exit_reason
            }
            self.position = None
            return trade

        return None
