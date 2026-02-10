import json
import threading
import websocket
import time
from smarttradex_core.data.candle_buffer import candle_buffer


# ============================================================
# CONFIG
# ============================================================

SYMBOL = "btcusdt"
INTERVAL = "1m"

BINANCE_WS = f"wss://stream.binance.com:9443/ws/{SYMBOL}@kline_{INTERVAL}"

_ws_thread = None
_running = False


# ============================================================
# WEBSOCKET EVENTS
# ============================================================

def _on_message(ws, message):
    global candle_buffer

    try:
        data = json.loads(message)

        if "k" not in data:
            return

        k = data["k"]

        candle = {
            "time": int(k["t"]),
            "open": float(k["o"]),
            "high": float(k["h"]),
            "low": float(k["l"]),
            "close": float(k["c"]),
            "volume": float(k["v"]),
            "closed": bool(k["x"])
        }

        # push candle into buffer (handles partial + closed automatically)
        candle_buffer.update(candle)

    except Exception as e:
        print("WS parse error:", e)


def _on_error(ws, error):
    print("WS error:", error)


def _on_close(ws, close_status_code, close_msg):
    print("WS closed")


def _on_open(ws):
    print("WS connected")


# ============================================================
# WS LOOP
# ============================================================

def _run():
    global _running

    while _running:
        try:
            ws = websocket.WebSocketApp(
                BINANCE_WS,
                on_message=_on_message,
                on_error=_on_error,
                on_close=_on_close
            )
            ws.on_open = _on_open
            ws.run_forever()

        except Exception as e:
            print("WS restart:", e)

        time.sleep(3)


# ============================================================
# PUBLIC CONTROL
# ============================================================

def start_ws_client():
    global _ws_thread, _running

    if _running:
        return

    _running = True
    _ws_thread = threading.Thread(target=_run, daemon=True)
    _ws_thread.start()

    print("WS client started")


def stop_ws_client():
    global _running
    _running = False
    print("WS client stopped")
