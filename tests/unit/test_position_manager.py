from smarttradex_core.trading.position_manager import PositionManager

pm = PositionManager()

assert not pm.has_position()

opened = pm.open_position("BUY", 100)
assert opened is True
assert pm.has_position()

# cannot open another position
opened_again = pm.open_position("BUY", 101)
assert opened_again is False

closed = pm.close_position(110)
assert closed["entry_price"] == 100
assert closed["exit_price"] == 110
assert not pm.has_position()

print("PositionManager test passed")
