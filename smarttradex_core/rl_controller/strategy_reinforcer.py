class StrategyReinforcer:
    """
    Adjusts strategy weighting based on performance
    """

    def __init__(self):

        self.stats = {}

    # --------------------------------------------------
    # RECORD TRADE OUTCOME
    # --------------------------------------------------
    def record_trade(self, strategy, pnl):

        if strategy not in self.stats:
            self.stats[strategy] = {
                "trades": 0,
                "wins": 0,
                "pnl": 0
            }

        self.stats[strategy]["trades"] += 1
        self.stats[strategy]["pnl"] += pnl

        if pnl > 0:
            self.stats[strategy]["wins"] += 1

    # --------------------------------------------------
    # WIN RATE
    # --------------------------------------------------
    def win_rate(self, strategy):

        s = self.stats.get(strategy)

        if not s or s["trades"] == 0:
            return 0.5

        return s["wins"] / s["trades"]

    # --------------------------------------------------
    # STRATEGY WEIGHT
    # --------------------------------------------------
    def weight(self, strategy):

        wr = self.win_rate(strategy)

        if wr > 0.65:
            return 1.2   # boost

        elif wr < 0.45:
            return 0.7   # penalty

        return 1.0       # neutral

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------
    def summary(self):

        output = {}

        for strat in self.stats:

            output[strat] = {
                "win_rate": round(
                    self.win_rate(strat), 2
                ),
                "weight": self.weight(strat),
                "trades": self.stats[strat]["trades"]
            }

        return output
