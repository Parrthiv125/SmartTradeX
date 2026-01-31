from smarttradex_core.engine import TradingEngine

engine = TradingEngine()

# Start engine
engine.start()

# Add 5 fake 1-minute candles
for i in range(5):
    engine.candle_buffer.add_candle({
        "timestamp": i,
        "open": 100,
        "high": 110,
        "low": 90,
        "close": 110,
        "volume": 10
    })

# Run one engine step (no real market call)
engine.running = True

# Manually call feature logic (simulate step logic)
candle_5m = engine.candle_buffer.get_last_5m_candle()
features_5m = engine.feature_engine.build_5m_features(candle_5m)

assert features_5m is not None
assert "return_5m" in features_5m
assert features_5m["return_5m"] == 0.10

print("Engine 5-minute feature integration test PASSED")
