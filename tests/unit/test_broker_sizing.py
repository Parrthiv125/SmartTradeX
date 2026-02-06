from smarttradex_core.trading.paper_broker import PaperBroker

def run_test():

    broker = PaperBroker()

    # Simulate BUY marker
    marker_buy = {"action": "BUY"}
    broker.process_marker(marker_buy, 50000)

    print("Position:", broker.position)

    assert broker.position["qty"] > 0

    # Simulate price rise → TP exit
    marker_hold = {"action": "HOLD"}
    trade = broker.process_marker(marker_hold, 51000)

    print("Trade closed:", trade)

    assert trade is not None
    print("Broker sizing integration test passed")

if __name__ == "__main__":
    run_test()
