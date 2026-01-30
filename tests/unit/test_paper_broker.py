from smarttradex_core.trading.paper_broker import PaperBroker

broker = PaperBroker()

# BUY signal opens trade
broker.process_marker({"action": "BUY"}, price=100)

# SELL signal closes trade
trade = broker.process_marker({"action": "SELL"}, price=110)

assert trade is not None
assert trade["entry_price"] == 100
assert trade["exit_price"] == 110
assert trade["pnl"] == 10

assert len(broker.get_trades()) == 1

print("PaperBroker test passed")
