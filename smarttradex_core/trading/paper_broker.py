# smarttradex_core/trading/paper_broker.py

from smarttradex_core.trading.position_manager import PositionManager
from smarttradex_core.trading.order_simulator import OrderSimulator
from smarttradex_core.trading.pnl_calculator import PnLCalculator


class PaperBroker:
    """
    Coordinates paper trading execution.
    """

    def __init__(self):
        self.position_manager = PositionManager()
        self.order_simulator = OrderSimulator(self.position_manager)
        self.pnl_calculator = PnLCalculator()
        self.trades = []

    def process_marker(self, marker: dict, price: float):
        """
        Process a marker at a given price.
        """
        result = self.order_simulator.execute(marker, price)

        # trade closed
        if isinstance(result, dict):
            pnl = self.pnl_calculator.calculate(result)
            trade = {**result, **pnl}
            self.trades.append(trade)
            return trade

        return None

    def get_trades(self):
        return self.trades
