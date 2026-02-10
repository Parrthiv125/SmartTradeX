import requests
import time

# ============================================================
# SmartTradeX API Client
# GUI → FastAPI → Engine / Binance
# REAL DATA – PAPER TRADING (SAFE)
# ============================================================

BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 8


# ============================================================
# SAFE REQUEST HANDLER (AUTO-REFRESH FRIENDLY)
# ============================================================

def safe_get(endpoint, retries=2, delay=0.3):
    url = f"{BASE_URL}{endpoint}"

    for _ in range(retries):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except Exception:
            time.sleep(delay)

    return None


# ============================================================
# REAL BINANCE CANDLES (TIMEFRAME SUPPORT)
# ============================================================

def get_candles(interval="5m", limit=200):
    """
    Fetch REAL Binance OHLCV candles with selectable timeframe.

    limit:
        number of candles requested (default 200)
    """
    return safe_get(f"/market/candles?interval={interval}&limit={limit}")


# ============================================================
# FAST REFRESH (LAST CANDLE ONLY)
# ============================================================

def get_last_candle(interval="5m"):
    """
    Fetch ONLY the most recent candle.
    Used for smooth streaming updates.
    """
    data = safe_get(f"/market/candles?interval={interval}&limit=1")
    if data and "candles" in data and len(data["candles"]) > 0:
        return data["candles"][0]
    return None


# ============================================================
# REAL BINANCE LIVE PRICE (TICKER)
# ============================================================

def get_live_price(symbol="BTCUSDT"):
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": symbol}

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()

    return float(response.json()["price"])


# ============================================================
# STRATEGY MARKERS (PAPER TRADING)
# ============================================================

def get_markers():
    return safe_get("/markers") or []


# ============================================================
# PAPER TRADES
# ============================================================

def get_trades():
    return safe_get("/trades") or []


def get_positions():
    return []


# ============================================================
# ENGINE STATE
# ============================================================

def get_state():
    return safe_get("/state") or {}


# ============================================================
# ENGINE CONTROLS
# ============================================================

def start_engine():
    response = requests.post(
        f"{BASE_URL}/engine/start",
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def stop_engine():
    response = requests.post(
        f"{BASE_URL}/engine/stop",
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def reset_engine():
    return {"status": "ok"}
