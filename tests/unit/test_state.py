from smarttradex_core.state import EngineState

state = EngineState()

snap = state.snapshot()
assert snap["market_data"] is None
assert snap["markers"] == []
assert snap["trades"] == []

state.markers.append({"action": "BUY"})
state.trades.append({"pnl": 10})

snap = state.snapshot()
assert len(snap["markers"]) == 1
assert len(snap["trades"]) == 1

print("EngineState snapshot test passed")
