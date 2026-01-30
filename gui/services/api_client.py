# gui/services/api_client.py

import requests

BASE_URL = "http://127.0.0.1:8000"


def get_engine_status():
    response = requests.get(f"{BASE_URL}/engine/status")
    return response.json()


def get_engine_config():
    response = requests.get(f"{BASE_URL}/engine/config")
    return response.json()


def start_engine():
    return requests.post(f"{BASE_URL}/engine/start", timeout=5)

def stop_engine():
    return requests.post(f"{BASE_URL}/engine/stop", timeout=5)

def reset_engine():
    return requests.post(f"{BASE_URL}/engine/reset", timeout=5)

def get_state():
    return requests.get(f"{BASE_URL}/state", timeout=5).json()


def get_positions():
    response = requests.get(f"{BASE_URL}/trading/positions")
    return response.json()


def get_trades():
    response = requests.get(f"{BASE_URL}/trading/trades")
    return response.json()


def get_pnl():
    response = requests.get(f"{BASE_URL}/trading/pnl")
    return response.json()


def get_markers():
    response = requests.get(f"{BASE_URL}/markers")
    return response.json()

