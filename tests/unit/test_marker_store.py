from smarttradex_core.markers.marker_store import MarkerStore

store = MarkerStore()

assert store.get_all() == []

store.add({"action": "BUY"})
store.add({"action": "SELL"})

assert len(store.get_all()) == 2

store.clear()
assert store.get_all() == []

print("MarkerStore test passed")
