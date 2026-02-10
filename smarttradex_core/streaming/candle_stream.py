import json
import websocket
import threading

LATEST_CANDLES = []
RUNNING = False

BINANCE_WS = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"


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

    LATEST_CANDLES.append(candle)

    if len(LATEST_CANDLES) > 500:
        LATEST_CANDLES.pop(0)


def _run_ws():
    ws = websocket.WebSocketApp(
        BINANCE_WS,
        on_message=_on_message
    )
    ws.run_forever()


def start_candle_stream():
    global RUNNING

    if RUNNING:
        return

    RUNNING = True
    thread = threading.Thread(target=_run_ws, daemon=True)
    thread.start()


def get_live_candles():
    return LATEST_CANDLES
