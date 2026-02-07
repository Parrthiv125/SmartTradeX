from smarttradex_core.features.feature_engine import FeatureEngine


def run_test():

    engine = FeatureEngine()

    candles = []

    price = 50000

    for i in range(60):
        candles.append({"close": price + i * 10})

    features = engine.build_features(candles)

    print(features)

    assert features is not None
    print("Expanded feature test passed")


if __name__ == "__main__":
    run_test()
