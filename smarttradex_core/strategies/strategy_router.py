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

        self.momentum = MomentumStrategy()
        self.mean_reversion = MeanReversionStrategy()
        self.breakout = BreakoutStrategy()
        self.swing = SwingStrategy()

    # ─────────────────────────────────────────────
    # ROUTING LOGIC
    # ─────────────────────────────────────────────
    def route(self, prediction: dict, regime: str):

        if regime == "trend":
            return self.momentum.generate_signal(prediction)

        elif regime == "range":
            return self.mean_reversion.generate_signal(prediction)

        elif regime == "volatile":
            return self.breakout.generate_signal(prediction)

        else:
            return self.swing.generate_signal(prediction)
