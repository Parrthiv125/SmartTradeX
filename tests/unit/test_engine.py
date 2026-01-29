from smarttradex_core.engine import TradingEngine

engine = TradingEngine()

assert engine.running is False

engine.start()
assert engine.running is True

engine.stop()
assert engine.running is False

engine.reset()

print("TradingEngine test passed")
