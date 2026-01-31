import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from smarttradex_core.prediction.predictor import Predictor

predictor = Predictor()

features_1m = {"return_1m": 0.01}
features_5m = {"return_5m": 0.05}

prediction = predictor.predict(features_1m, features_5m)

assert prediction["action"] == "BUY"
assert prediction["confidence"] == 0.6

print("Predictor 5-minute feature test PASSED")
