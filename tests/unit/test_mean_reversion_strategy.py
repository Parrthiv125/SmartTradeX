from smarttradex_core.strategies.mean_reversion import MeanReversionStrategy


def run_test():

    strategy = MeanReversionStrategy()

    # Weak BUY → SELL
    signal = strategy.generate_signal({
        "action": "BUY",
        "confidence": 0.5
    })

    assert signal["action"] == "SELL"
    print("BUY reversed ✔️")

    # Strong BUY → HOLD
    signal = strategy.generate_signal({
        "action": "BUY",
        "confidence": 0.9
    })

    assert signal["action"] == "HOLD"
    print("Strong trend ignored ✔️")


if __name__ == "__main__":
    run_test()
