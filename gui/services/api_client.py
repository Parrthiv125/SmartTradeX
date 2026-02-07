import requests

BASE_URL = "http://127.0.0.1:8000"

# --------------------------------
# MARKET DATA
# --------------------------------

def get_candles():
    response = requests.get(f"{BASE_URL}/market/candles")
    return response.json()


# --------------------------------
# MARKERS
# --------------------------------

def get_markers():
    response = requests.get(f"{BASE_URL}/markers")
    return response.json()


# --------------------------------
# TRADES & POSITIONS
# --------------------------------

def get_trades():
    response = requests.get(f"{BASE_URL}/trades")
    return response.json()


def get_positions():
    # Positions not implemented yet (safe stub)
    return []


# --------------------------------
# ENGINE STATE
# --------------------------------

def get_state():
    response = requests.get(f"{BASE_URL}/state")
    return response.json()


# --------------------------------
# ENGINE CONTROLS
# --------------------------------

def start_engine():
    response = requests.post(f"{BASE_URL}/engine/start")
    return response.json()


def stop_engine():
    response = requests.post(f"{BASE_URL}/engine/stop")
    return response.json()


def reset_engine():
    # Reset not implemented yet (safe stub)
    return {"status": "ok"}
