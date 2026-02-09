import threading
import pandas as pd
from collections import deque
from datetime import datetime

# ------------------------------------------
# GLOBAL CANDLE BUFFER
# ------------------------------------------

MAX_CANDLES = 500
_lock = threading.Lock()

candle_buffer = deque(maxlen=MAX_CANDLES)


# ------------------------------------------
# ADD / UPDATE CANDLE
# ------------------------------------------

def update_candle(candle):
    """
    candle = {
        "timestamp": int(ms),
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float
    }
    """
    with _lock:
        if len(candle_buffer) > 0:
            last = candle_buffer[-1]

            # update same candle
            if last["timestamp"] == candle["timestamp"]:
                candle_buffer[-1] = candle
                return

        candle_buffer.append(candle)


# ------------------------------------------
# GET DATAFRAME
# ------------------------------------------

def get_candle_dataframe():
    with _lock:
        if not candle_buffer:
            return pd.DataFrame()

        df = pd.DataFrame(list(candle_buffer))
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
