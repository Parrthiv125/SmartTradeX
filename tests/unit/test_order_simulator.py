from smarttradex_core.trading.position_manager import PositionManager
from smarttradex_core.trading.order_simulator import OrderSimulator

pm = PositionManager()
sim = OrderSimulator(pm)

# BUY opens position
result = sim.execute({"action": "BUY"}, price=100)
assert result is True
assert pm.has_position()

# SELL closes position
closed = sim.execute({"action": "SELL"}, price=110)
assert closed["exit_price"] == 110
assert not pm.has_position()

# HOLD does nothing
result = sim.execute({"action": "HOLD"}, price=120)
assert result is None

print("OrderSimulator test passed")
