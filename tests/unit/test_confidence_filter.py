from smarttradex_core.trading.paper_broker import PaperBroker


def run_test():

    broker = PaperBroker()
    price = 50000

    # LOW confidence → should NOT enter
    broker.process_marker(
        {"action": "BUY", "confidence": 0.40},
        price
    )

    assert broker.position is None
    print("Low confidence blocked ✔️")

    # HIGH confidence → should enter
    broker.process_marker(
        {"action": "BUY", "confidence": 0.80},
        price
    )

    assert broker.position is not None
    print("High confidence entry ✔️")


if __name__ == "__main__":
    run_test()
