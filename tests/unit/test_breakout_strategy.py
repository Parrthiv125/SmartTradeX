from smarttradex_core.strategies.breakout import BreakoutStrategy


def run_test():

    strategy = BreakoutStrategy()

    # Strong BUY breakout
    signal = strategy.generate_signal({
        "action": "BUY",
        "confidence": 0.85
    })

    assert signal["action"] == "BUY"
    print("Breakout BUY ✔️")

    # Weak signal ignored
    signal = strategy.generate_signal({
        "action": "BUY",
        "confidence": 0.5
    })

    assert signal["action"] == "HOLD"
    print("Weak breakout ignored ✔️")


if __name__ == "__main__":
    run_test()
