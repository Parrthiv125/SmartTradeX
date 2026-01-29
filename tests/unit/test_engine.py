from smarttradex_core.engine import TradingEngine

engine = TradingEngine()

engine.start()

prediction = engine.step()

assert prediction is not None
assert engine.state.market_data is not None
assert engine.state.prediction == prediction

engine.stop()

print("TradingEngine AI pipeline integration test passed")
