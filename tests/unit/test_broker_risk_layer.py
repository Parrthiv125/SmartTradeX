import time
from smarttradex_core.trading.paper_broker import PaperBroker


def run_test():

    broker = PaperBroker()
    price = 50000

    # Entry allowed
    broker.process_marker(
        {"action": "BUY", "confidence": 0.9},
        price
    )

    assert broker.position is not None
    print("Entry allowed ✔️")

    # Exit trade
    broker.process_marker(
        {"action": "SELL", "confidence": 0.9},
        price * 1.02
    )

    # Immediate re-entry blocked
    broker.process_marker(
        {"action": "BUY", "confidence": 0.9},
        price
    )

    assert broker.position is None
    print("Cooldown working ✔️")


if __name__ == "__main__":
    run_test()
