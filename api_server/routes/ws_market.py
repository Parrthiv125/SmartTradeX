from fastapi import APIRouter, WebSocket
import websocket
import asyncio
import json

router = APIRouter()

BINANCE_WS = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"


@router.websocket("/ws/market")
async def market_stream(ws: WebSocket):
    await ws.accept()

    async with websocket.connect(BINANCE_WS) as binance_ws:

        while True:
            data = await binance_ws.recv()
            message = json.loads(data)

            k = message["k"]

            candle = {
                "time": k["t"],
                "open": float(k["o"]),
                "high": float(k["h"]),
                "low": float(k["l"]),
                "close": float(k["c"]),
                "closed": k["x"]
            }

            await ws.send_json(candle)
