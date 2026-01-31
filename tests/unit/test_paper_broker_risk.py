import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from smarttradex_core.trading.paper_broker import PaperBroker

broker = PaperBroker()

# Enter trade
broker.process_marker({"action": "BUY"}, 100)

# Price goes up → take profit
trade = broker.process_marker({"action": "HOLD"}, 102)

assert trade is not None
assert trade["reason"] == "TAKE_PROFIT"

print("PaperBroker stop-loss / take-profit test PASSED")
