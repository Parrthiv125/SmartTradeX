import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from smarttradex_core.trading.paper_broker import PaperBroker

broker = PaperBroker()

# Enter trade
broker.process_marker({"action": "BUY"}, 100)

# Exit via take profit
trade = broker.process_marker({"action": "HOLD"}, 102)

assert trade is not None

history = broker.get_trade_history()
assert len(history) == 1
assert history[0]["pnl_pct"] == 0.02

print("PaperBroker trade history test PASSED")
