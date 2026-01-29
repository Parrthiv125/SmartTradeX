# smarttradex_core/engine.py

from smarttradex_core.state import EngineState


class TradingEngine:
    def __init__(self):
        self.state = EngineState()
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        print("Engine started")

    def stop(self):
        if not self.running:
            return
        self.running = False
        print("Engine stopped")

    def reset(self):
        self.state.reset()
        print("Engine state reset")
