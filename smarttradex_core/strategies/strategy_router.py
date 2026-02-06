from smarttradex_core.strategies.momentum import MomentumStrategy
from smarttradex_core.strategies.mean_reversion import MeanReversionStrategy
from smarttradex_core.strategies.breakout import BreakoutStrategy
from smarttradex_core.strategies.swing import SwingStrategy


class StrategyRouter:
    """
    Routes prediction signals to appropriate strategy
    based on detected market regime.
    """

    def __init__(self):

        # Initialize all strategies
        self.momentum = MomentumStrategy()
        self.mean_reversion = MeanReversionStrategy()
        self.breakout = BreakoutStrategy()
        self.swing = SwingStrategy()

    # ─────────────────────────────────────────────
    # MAIN ROUTING FUNCTION
    # ─────────────────────────────────────────────
    def route(self, prediction: dict, regime: str):
        """
        Routes prediction to the correct strategy.

        :param prediction: predictor output
        :param regime: market regime (trend / range / volatile)
        :return: marker dict
        """

        if regime == "trend":
            return self.momentum.generate_signal(prediction)

        elif regime == "range":
            return self.mean_reversion.generate_signal(prediction)

        elif regime == "volatile":
            return self.breakout.generate_signal(prediction)

        else:
            # Default fallback
            return self.swing.generate_signal(prediction)
