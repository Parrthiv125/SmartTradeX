from smarttradex_core.engine import TradingEngine

engine = TradingEngine()
engine.start()

# BUY step
result1 = engine.step()
assert "marker" in result1

# SELL step (close trade)
result2 = engine.step()

if result2["trade"]:
    trade = result2["trade"]
    assert "pnl" in trade

engine.stop()

print("TradingEngine paper trading integration test passed")
