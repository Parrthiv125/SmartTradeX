import websocket
import json
import threading
import time
import requests

BACKEND_WS_URL = "ws://localhost:8000/ws/candles"


def _listen():
    while True:
        try:
            ws = websocket.create_connection(BACKEND_WS_URL)

            while True:
                data = ws.recv()
                candle = json.loads(data)

                # push to backend buffer endpoint
                requests.post(
                    "http://localhost:8000/internal/update-candle",
                    json=candle,
                    timeout=2,
                )

        except Exception:
            time.sleep(3)


def start_ws_client():
    t = threading.Thread(target=_listen, daemon=True)
    t.start()
