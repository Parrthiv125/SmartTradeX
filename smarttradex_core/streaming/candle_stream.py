import json
import websocket
import threading
import requests

from smarttradex_core.prediction.predictor import Predictor
from smarttradex_core.strategies.strategy_router import StrategyRouter
from smarttradex_core.features.feature_engine import FeatureEngine


# -----------------------------------
# INIT CORE COMPONENTS
# -----------------------------------

predictor = Predictor()
router = StrategyRouter()
feature_engine = FeatureEngine()


# -----------------------------------
# GLOBAL BUFFERS
# -----------------------------------

LATEST_CANDLES = []
RUNNING = False


BINANCE_WS = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"


# -----------------------------------
# LOAD HISTORICAL CANDLES (BOOTSTRAP ML)
# -----------------------------------

def load_historical_candles(limit=200):

    url = (
        "https://api.binance.com/api/v3/klines"
        "?symbol=BTCUSDT&interval=1m"
        f"&limit={limit}"
    )

    response = requests.get(url)
    data = response.json()

    candles = []

    for k in data:
        candles.append({
            "time": k[0],
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4])
        })

    return candles


# -----------------------------------
# CANDLE MESSAGE HANDLER
# -----------------------------------

def _on_message(ws, message):
    global LATEST_CANDLES

    data = json.loads(message)
    k = data["k"]

    candle = {
        "time": k["t"],
        "open": float(k["o"]),
        "high": float(k["h"]),
        "low": float(k["l"]),
        "close": float(k["c"])
    }

    # -----------------------------------
    # STORE CANDLE FIRST
    # -----------------------------------

    LATEST_CANDLES.append(candle)

    if len(LATEST_CANDLES) > 500:
        LATEST_CANDLES.pop(0)


    # -----------------------------------
    # BUILD FEATURES
    # -----------------------------------

    try:

        features = feature_engine.build_features(
            LATEST_CANDLES
        )

        # If not enough candles yet, skip
        if not features:
            return

        # Inject timestamp for overlay
        features["time"] = candle["time"]

        # -----------------------------------
        # ML PREDICTION
        # -----------------------------------

        prediction = predictor.predict(features)

        # Merge prediction + features
        prediction["time"] = candle["time"]

        # -----------------------------------
        # STRATEGY ROUTING
        # -----------------------------------

        router.route(
            prediction,
            regime="trend"
        )

    except Exception as e:
        print("Prediction execution error:", e)


# -----------------------------------
# WEBSOCKET RUNNER
# -----------------------------------

def _run_ws():

    ws = websocket.WebSocketApp(
        BINANCE_WS,
        on_message=_on_message
    )

    ws.run_forever()


# -----------------------------------
# START STREAM
# -----------------------------------

def start_candle_stream():
    global RUNNING, LATEST_CANDLES

    if RUNNING:
        return

    print("Loading historical candles...")

    # Bootstrap history → ML active instantly
    LATEST_CANDLES = load_historical_candles(200)

    print(f"Loaded {len(LATEST_CANDLES)} candles")

    RUNNING = True

    thread = threading.Thread(
        target=_run_ws,
        daemon=True
    )
    thread.start()


# -----------------------------------
# LIVE CANDLE ACCESS (API)
# -----------------------------------

def get_live_candles():
    return LATEST_CANDLES
