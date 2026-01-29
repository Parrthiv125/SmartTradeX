from smarttradex_core.engine import TradingEngine
from smarttradex_core.lifecycle import EngineLifecycle

engine = TradingEngine()
lifecycle = EngineLifecycle(engine)

lifecycle.start()
assert engine.running is True

lifecycle.stop()
assert engine.running is False

lifecycle.reset()

print("EngineLifecycle test passed")
