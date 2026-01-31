from smarttradex_core.features.feature_engine import FeatureEngine

engine = FeatureEngine()

fake_5m_candle = {
    "open": 100,
    "close": 110
}

features = engine.build_5m_features(fake_5m_candle)

assert "return_5m" in features
assert features["return_5m"] == 0.10

print("5-minute feature engine test PASSED")
