# =========================================
# SmartTradeX — Main FastAPI Entry
# =========================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# =========================================
# API ROUTE IMPORTS
# =========================================

from api_server.routes import engine as engine_routes
from api_server.routes import state as state_routes
from api_server.routes import trading as trading_routes
from api_server.routes import markers as markers_routes
from api_server.routes import config as config_routes
from api_server.routes import market as market_routes
from api_server.routes import analytics as analytics_routes
from api_server.routes import predictions
from api_server.routes.auth import router as auth_router


# =========================================
# FASTAPI APP INIT
# =========================================

app = FastAPI(
    title="SmartTradeX API",
    version="1.0.0"
)


# =========================================
# CORS CONFIGURATION
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Dev mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# MOCK ENGINE (TEMPORARY ENGINE STATE)
# =========================================

class MockEngine:

    def status(self):
        return "stopped"

    def is_running(self):
        return False


class MockRuntime:

    def __init__(self):
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running


# Attach mock runtime to app state
app.state.engine = MockEngine()
app.state.runtime = MockRuntime()


# =========================================
# ROUTER REGISTRATION
# =========================================

# Engine Control
app.include_router(engine_routes.router)

# Engine State
app.include_router(state_routes.router)

# Engine Config
app.include_router(config_routes.router)

# Trading Execution
app.include_router(trading_routes.router)

# Trade Markers / Overlays
app.include_router(markers_routes.router)

# Market Data / Candles / Orderbook
app.include_router(market_routes.router)

# Predictions
app.include_router(predictions.router)

# Authentication
app.include_router(auth_router)

# Analytics (Portfolio / Trades / Metrics)
app.include_router(analytics_routes.router)


# =========================================
# HEALTH CHECK
# =========================================

@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "engine": app.state.engine.status(),
        "running": app.state.runtime.is_running()
    }
