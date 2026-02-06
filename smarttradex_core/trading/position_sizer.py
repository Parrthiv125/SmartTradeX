# smarttradex_core/trading/position_sizer.py

class PositionSizer:
    """
    Calculates position size based on account capital.
    Beginner-safe fixed % allocation model.
    """

    def __init__(self, capital: float, risk_per_trade: float = 0.02):
        """
        :param capital: Total paper trading capital
        :param risk_per_trade: % capital to allocate per trade (0.02 = 2%)
        """
        self.capital = capital
        self.risk_per_trade = risk_per_trade

    def update_capital(self, new_capital: float):
        """Update capital after trade closes."""
        self.capital = new_capital

    def calculate_position_size(self, price: float) -> float:
        """
        Returns quantity to buy/sell based on capital allocation.
        """
        if price <= 0:
            return 0

        allocation = self.capital * self.risk_per_trade
        quantity = allocation / price

        return round(quantity, 6)
