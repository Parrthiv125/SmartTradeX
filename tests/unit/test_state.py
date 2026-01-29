from smarttradex_core.state import EngineState

state = EngineState()

assert state.market_data is None
assert state.position is None

state.markers.append("test_marker")
assert len(state.markers) == 1

state.reset()
assert len(state.markers) == 0

print("EngineState test passed")
