import requests
import time

BASE_URL = "http://127.0.0.1:8000"

# ─────────────────────────────────────────────
# INTERNAL SAFE REQUEST WRAPPER
# ─────────────────────────────────────────────

def safe_get(endpoint, retries=2, timeout=8):
    url = f"{BASE_URL}{endpoint}"

    for _ in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except Exception:
            time.sleep(0.3)

    return None


def safe_post(endpoint, timeout=5):
    url = f"{BASE_URL}{endpoint}"

    try:
        return requests.post(url, timeout=timeout)
    except Exception:
        return None


# ─────────────────────────────────────────────
# ENGINE
# ─────────────────────────────────────────────

def get_engine_status():
    data = safe_get("/engine/status")
    return data or {}


def get_engine_config():
    data = safe_get("/engine/config")
    return data or {}


def start_engine():
    return safe_post("/engine/start")


def stop_engine():
    return safe_post("/engine/stop")


def reset_engine():
    return safe_post("/engine/reset")


# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────

def get_state():
    data = safe_get("/state")
    return data or {}


# ─────────────────────────────────────────────
# TRADING
# ─────────────────────────────────────────────

def get_positions():
    data = safe_get("/trading/positions")
    return data or {}


def get_trades():
    data = safe_get("/trading/trades")
    if data:
        return data.get("trades", [])
    return []


def get_pnl():
    data = safe_get("/trading/pnl")
    return data or {}


# ─────────────────────────────────────────────
# MARKERS
# ─────────────────────────────────────────────

def get_markers():
    data = safe_get("/markers")
    return data or {}
