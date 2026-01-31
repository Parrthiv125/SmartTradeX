import requests

BASE_URL = "http://127.0.0.1:8000"


def get_engine_status():
    try:
        return requests.get(f"{BASE_URL}/engine/status", timeout=5).json()
    except Exception:
        return {}


def get_engine_config():
    try:
        return requests.get(f"{BASE_URL}/engine/config", timeout=5).json()
    except Exception:
        return {}


def start_engine():
    return requests.post(f"{BASE_URL}/engine/start", timeout=5)


def stop_engine():
    return requests.post(f"{BASE_URL}/engine/stop", timeout=5)


def reset_engine():
    return requests.post(f"{BASE_URL}/engine/reset", timeout=5)


def get_state():
    try:
        return requests.get(f"{BASE_URL}/state", timeout=5).json()
    except Exception:
        return {}


def get_positions():
    try:
        return requests.get(f"{BASE_URL}/trading/positions", timeout=5).json()
    except Exception:
        return {}


def get_trades():
    """
    Task 1:
    Fetch real paper trades from API and return trade list only.
    """
    try:
        response = requests.get(f"{BASE_URL}/trading/trades", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("trades", [])
    except Exception:
        return []


def get_pnl():
    try:
        return requests.get(f"{BASE_URL}/trading/pnl", timeout=5).json()
    except Exception:
        return {}


def get_markers():
    try:
        return requests.get(f"{BASE_URL}/markers", timeout=5).json()
    except Exception:
        return {}