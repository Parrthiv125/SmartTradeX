# smarttradex_core/lifecycle.py

from smarttradex_core.engine import TradingEngine


class EngineLifecycle:
    def __init__(self, engine: TradingEngine):
        self.engine = engine

    def start(self):
        self.engine.start()

    def stop(self):
        self.engine.stop()

    def reset(self):
        self.engine.reset()
