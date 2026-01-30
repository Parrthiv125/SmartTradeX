# smarttradex_core/trading/position_manager.py

class PositionManager:
    """
    Tracks the current open position (paper trading).
    """

    def __init__(self):
        self.position = None

    def open_position(self, side: str, price: float):
        if self.position is not None:
            return False  # position already open

        self.position = {
            "side": side,
            "entry_price": price
        }
        return True

    def close_position(self, price: float):
        if self.position is None:
            return None

        closed = {
            "side": self.position["side"],
            "entry_price": self.position["entry_price"],
            "exit_price": price
        }

        self.position = None
        return closed

    def has_position(self):
        return self.position is not None
