# smarttradex_core/trading/pnl_calculator.py

class PnLCalculator:
    """
    Calculates profit and loss for paper trades.
    """

    def calculate(self, trade: dict) -> dict:
        entry = trade["entry_price"]
        exit_ = trade["exit_price"]
        side = trade["side"]

        if side == "BUY":
            pnl = exit_ - entry
        else:
            pnl = entry - exit_

        pnl_pct = (pnl / entry) * 100 if entry != 0 else 0.0

        return {
            "pnl": pnl,
            "pnl_pct": pnl_pct
        }
