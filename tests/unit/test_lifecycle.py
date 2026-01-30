from smarttradex_core.engine import TradingEngine
from smarttradex_core.lifecycle import EngineRuntime
import threading
import time

engine = TradingEngine()
runtime = EngineRuntime(engine)

runtime.start()

# run loop in a separate thread JUST FOR TEST
t = threading.Thread(target=runtime.run_loop, args=(0.2,))
t.start()

time.sleep(0.6)
runtime.stop()
t.join()

print("Timed engine loop test passed")
