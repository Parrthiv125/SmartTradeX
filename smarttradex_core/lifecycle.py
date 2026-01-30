# smarttradex_core/lifecycle.py

import time


class EngineRuntime:
    """
    Controls the runtime execution of the trading engine.
    Beginner-safe: no threads, no async.
    """

    def __init__(self, engine):
        self.engine = engine
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        self.engine.start()

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.engine.stop()

    def run_once(self):
        """
        Run exactly ONE engine step.
        Safe for API / GUI control.
        """
        if not self.running:
            return None
        return self.engine.step()
