from smarttradex_core.features.feature_engine import FeatureEngine

engine = FeatureEngine()

features = engine.build_features([])
assert features == {}

sample_candles = [
    {"close": 100},
    {"close": 101},
    {"close": 102},
]

features = engine.build_features(sample_candles)

assert features["num_candles"] == 3
assert features["last_close"] == 102
assert "dummy_feature" in features

print("FeatureEngine skeleton test passed")

