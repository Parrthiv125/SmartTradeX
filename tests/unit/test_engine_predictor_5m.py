import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from smarttradex_core.engine import TradingEngine

engine = TradingEngine()
engine.start()

# Add 5 candles with upward move
for i in range(5):
    engine.candle_buffer.add_candle({
        "timestamp": i,
        "open": 100,
        "high": 110,
        "low": 90,
        "close": 110,
        "volume": 10
    })

# Fake market update bypass
engine.running = True

# Manually inject feature logic
candle_5m = engine.candle_buffer.get_last_5m_candle()
features_5m = engine.feature_engine.build_5m_features(candle_5m)

features_1m = {"return_1m": 0.01}

prediction = engine.predictor.predict(features_1m, features_5m)

assert prediction["action"] == "BUY"

print("Engine predictor 5-minute wiring test PASSED")
