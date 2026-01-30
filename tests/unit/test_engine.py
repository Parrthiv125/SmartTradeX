from smarttradex_core.engine import TradingEngine

engine = TradingEngine()

engine.start()

marker = engine.step()

assert marker is not None
assert "action" in marker
assert engine.state.prediction is not None
assert len(engine.state.markers) == 1

engine.stop()

print("TradingEngine marker integration test passed")
