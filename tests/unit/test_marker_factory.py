from smarttradex_core.markers.marker_factory import MarkerFactory

factory = MarkerFactory(threshold=0.1)

buy = factory.create_marker({"predicted_delta_pct": 0.2, "confidence": 0.9})
assert buy["action"] == "BUY"

sell = factory.create_marker({"predicted_delta_pct": -0.2, "confidence": 0.8})
assert sell["action"] == "SELL"

hold = factory.create_marker({"predicted_delta_pct": 0.05, "confidence": 0.5})
assert hold["action"] == "HOLD"

print("MarkerFactory skeleton test passed")
