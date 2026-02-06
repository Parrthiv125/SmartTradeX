from smarttradex_core.strategies.swing import SwingStrategy


def run_test():

    strategy = SwingStrategy()

    # Mid confidence BUY
    signal = strategy.generate_signal({
        "action": "BUY",
        "confidence": 0.65
    })

    assert signal["action"] == "BUY"
    print("Swing BUY ✔️")

    # Low confidence → HOLD
    signal = strategy.generate_signal({
        "action": "BUY",
        "confidence": 0.3
    })

    assert signal["action"] == "HOLD"
    print("Low confidence HOLD ✔️")


if __name__ == "__main__":
    run_test()
