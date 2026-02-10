from smarttradex_core.analytics.accuracy_tracker import AccuracyTracker


tracker = AccuracyTracker(window_size=10)

# Simulate predictions
tracker.record_prediction(0.002, 0.003)
tracker.record_prediction(-0.001, 0.002)
tracker.record_prediction(0.004, 0.001)

print(tracker.summary())
