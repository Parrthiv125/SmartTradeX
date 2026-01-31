# api_server/main.py

from fastapi import FastAPI

# =========================
# Core Engine
# =========================
from smarttradex_core.engine import TradingEngine
from smarttradex_core.lifecycle import EngineRuntime

# =========================
# API Routes
# =========================
from api_server.routes import engine as engine_routes
from api_server.routes import state as state_routes
from api_server.routes import trading as trading_routes
from api_server.routes import markers as markers_routes
from api_server.routes import config as config_routes
from api_server.routes.trading import router as trading_router

# =========================
# FastAPI App
# =========================
app = FastAPI(title="SmartTradeX API")

# =========================
# SINGLE GLOBAL INSTANCES
# =========================
engine = TradingEngine()
runtime = EngineRuntime(engine)

app.state.engine = engine
app.state.runtime = runtime

# =========================
# Route Registration
# =========================
app.include_router(engine_routes.router)
app.include_router(state_routes.router)
app.include_router(config_routes.router)
app.include_router(trading_routes.router)
app.include_router(markers_routes.router)
app.include_router(trading_router)

# =========================
# Health Check
# =========================
@app.get("/health")
def health_check():
    return {"status": "ok"}
