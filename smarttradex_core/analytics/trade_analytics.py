from smarttradex_core.database.postgres_db import PostgresDB


class TradeAnalytics:

    def __init__(self):
        self.db = PostgresDB()

    # --------------------------------------------------
    def _get_closed_trades(self):

        query = """
        SELECT
            entry_price,
            exit_price,
            pnl_pct,
            pnl_value,
            strategy,
            entry_time,
            exit_time
        FROM paper_trades
        WHERE status = 'CLOSED'
        AND exit_price IS NOT NULL;
        """

        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    # --------------------------------------------------
    def total_trades(self):

        return len(self._get_closed_trades())

    # --------------------------------------------------
    def win_rate(self):

        trades = self._get_closed_trades()

        if not trades:
            return 0.0

        wins = [t for t in trades if t[3] and t[3] > 0]

        return (len(wins) / len(trades)) * 100

    # --------------------------------------------------
    def total_pnl(self):

        trades = self._get_closed_trades()

        return sum(t[3] or 0 for t in trades)

    # --------------------------------------------------
    def avg_pnl(self):

        trades = self._get_closed_trades()

        if not trades:
            return 0.0

        return (
            sum(t[3] or 0 for t in trades) /
            len(trades)
        )

    # --------------------------------------------------
    def max_drawdown(self):

        trades = self._get_closed_trades()

        equity = 10000
        peak = equity
        max_dd = 0

        for t in trades:

            pnl = t[3] or 0
            equity += pnl

            if equity > peak:
                peak = equity

            dd = peak - equity

            if dd > max_dd:
                max_dd = dd

        return max_dd

    # --------------------------------------------------
    def avg_trade_duration(self):

        trades = self._get_closed_trades()

        if not trades:
            return 0.0

        durations = []

        for t in trades:

            entry = t[5]
            exit_ = t[6]

            if entry and exit_:
                duration = (
                    exit_ - entry
                ).total_seconds()

                durations.append(duration)

        if not durations:
            return 0.0

        return sum(durations) / len(durations)

    # --------------------------------------------------
    def strategy_performance(self):

        trades = self._get_closed_trades()

        stats = {}

        for t in trades:

            strategy = t[4]
            pnl = t[3] or 0

            if strategy not in stats:
                stats[strategy] = {
                    "trades": 0,
                    "pnl": 0
                }

            stats[strategy]["trades"] += 1
            stats[strategy]["pnl"] += pnl

        return stats

    # --------------------------------------------------
    def summary(self):

        return {
            "total_trades": self.total_trades(),
            "win_rate": round(self.win_rate(), 2),
            "total_pnl": round(self.total_pnl(), 2),
            "avg_pnl": round(self.avg_pnl(), 2),
            "max_drawdown": round(self.max_drawdown(), 2),
            "avg_trade_duration_sec":
                round(self.avg_trade_duration(), 2),
            "strategy_performance":
                self.strategy_performance()
        }
