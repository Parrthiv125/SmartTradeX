import time
from smarttradex_core.streaming.candle_stream import start_candle_stream, get_live_candles

start_candle_stream()

while True:
    print(len(get_live_candles()))
    time.sleep(5)
