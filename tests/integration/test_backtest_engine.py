from smarttradex_core.backtesting.backtest_engine import BacktestEngine


engine = BacktestEngine(
    csv_path=r"D:\SmartTradeX\smarttradex_core\data\backtest_sample.csv"
)

engine.run()

print(engine.results())
