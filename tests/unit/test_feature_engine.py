from smarttradex_core.features.feature_engine import FeatureEngine


def run_test():

    engine = FeatureEngine()

    # Fake candle data
    candles = []

    price = 50000

    for i in range(25):
        candles.append({"close": price + i * 10})

    features = engine.build_features(candles)

    print(features)

    assert features is not None
    print("Feature engine ML test passed")


if __name__ == "__main__":
    run_test()
