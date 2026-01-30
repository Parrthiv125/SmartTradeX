# smarttradex_core/trading/order_simulator.py

from smarttradex_core.trading.position_manager import PositionManager


class OrderSimulator:
    """
    Simulates order execution using markers.
    """

    def __init__(self, position_manager: PositionManager):
        self.position_manager = position_manager

    def execute(self, marker: dict, price: float):
        action = marker.get("action")

        if action == "BUY":
            return self.position_manager.open_position("BUY", price)

        if action == "SELL":
            return self.position_manager.close_position(price)

        # HOLD or unknown action
        return None
