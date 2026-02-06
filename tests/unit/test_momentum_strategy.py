from smarttradex_core.strategies.momentum import MomentumStrategy


def run_test():

    strategy = MomentumStrategy()

    # High confidence BUY
    signal = strategy.generate_signal({
        "action": "BUY",
        "confidence": 0.8
    })

    assert signal["action"] == "BUY"
    print("BUY momentum ✔️")

    # Low confidence → HOLD
    signal = strategy.generate_signal({
        "action": "BUY",
        "confidence": 0.4
    })

    assert signal["action"] == "HOLD"
    print("Low confidence HOLD ✔️")


if __name__ == "__main__":
    run_test()
