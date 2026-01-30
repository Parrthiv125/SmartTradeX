from smarttradex_core.engine import TradingEngine
from smarttradex_core.lifecycle import EngineRuntime

engine = TradingEngine()
runtime = EngineRuntime(engine)

runtime.start()
result = runtime.run_once()

assert result is not None

runtime.stop()

print("EngineRuntime test passed")
