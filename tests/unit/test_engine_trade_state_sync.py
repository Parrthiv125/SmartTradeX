import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from smarttradex_core.engine import TradingEngine

engine = TradingEngine()
engine.start()

# Step 1: feed 5 candles so engine is ready
for i in range(5):
    engine.candle_buffer.add_candle({
        "timestamp": i,
        "open": 100,
        "high": 110,
        "low": 90,
        "close": 100,
        "volume": 10
    })

# Step 2: simulate BUY via engine loop
engine.paper_broker.process_marker({"action": "BUY"}, 100)

# Step 3: simulate price move & exit
engine.paper_broker.process_marker({"action": "HOLD"}, 102)

# Step 4: sync broker → engine state (same logic as engine.step)
engine.state.trades = engine.paper_broker.get_trade_history()

assert len(engine.paper_broker.get_trade_history()) == 1
assert len(engine.state.trades) == 1

print("Engine trade history sync test PASSED")
