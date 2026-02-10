import pandas as pd

from smarttradex_core.trading.paper_broker import PaperBroker
from smarttradex_core.analytics.trade_analytics import TradeAnalytics
from smarttradex_core.analytics.accuracy_tracker import AccuracyTracker


class BacktestEngine:
    """
    Runs historical backtests using live trading components
    """

    def __init__(self, csv_path):

        self.data = pd.read_csv(csv_path)

        self.broker = PaperBroker()
        self.analytics = TradeAnalytics()
        self.accuracy = AccuracyTracker()

    # --------------------------------------------------
    # RUN BACKTEST
    # --------------------------------------------------
    def run(self):

        print("Starting backtest...")

        for i in range(1, len(self.data)):

            price = self.data.iloc[i]["close"]

            predicted_return = self.data.iloc[i]["predicted_return"]
            actual_return = self.data.iloc[i]["actual_return"]

            # Accuracy tracking
            self.accuracy.record_prediction(
                predicted_return,
                actual_return
            )

            # Marker simulation
            marker = self.generate_marker(predicted_return)

            self.broker.process_marker(
                marker=marker,
                price=price
            )

        print("Backtest completed.")

    # --------------------------------------------------
    # SIMPLE MARKER GENERATION
    # --------------------------------------------------
    def generate_marker(self, predicted_return):

        if predicted_return > 0:
            return {
                "action": "BUY",
                "confidence": abs(predicted_return),
                "strategy": "Momentum"
            }

        else:
            return {
                "action": "SELL",
                "confidence": abs(predicted_return),
                "strategy": "Momentum"
            }

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------
    def results(self):

        return {
            "accuracy": self.accuracy.summary(),
            "analytics": self.analytics.summary(),
            "reinforcement":
                self.broker.get_reinforcement_summary()
        }
