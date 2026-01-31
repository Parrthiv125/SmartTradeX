import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import time
from smarttradex_core.trading.paper_broker import PaperBroker

broker = PaperBroker()

# Enter trade
broker.process_marker({"action": "BUY"}, 100)

# Force time passage
broker.position["entry_time"] -= 301  # > 5 minutes

trade = broker.process_marker({"action": "HOLD"}, 100)

assert trade is not None
assert trade["reason"] == "TIME_EXIT"

print("PaperBroker time-based exit test PASSED")
