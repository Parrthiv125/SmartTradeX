# api_server/main.py

from fastapi import FastAPI

# =========================
# Core Engine Imports
# (DO NOT MODIFY ENGINE CODE)
# =========================
from smarttradex_core.engine import TradingEngine
from smarttradex_core.runtime import EngineRuntime

# =========================
# API Route Imports
# =========================
from api_server.routes.engine import router as engine_router
from api_server.routes.state import router as state_router
from api_server.routes.trading import router as trading_router
from api_server.routes.markers import router as markers_router
from api_server.routes.config import router as config_router

# =========================
# FastAPI App
# =========================
app = FastAPI(title="SmartTradeX API")

# =========================
# SINGLE GLOBAL INSTANCES
# =========================
engine = TradingEngine()
runtime = EngineRuntime(engine)

# Expose to routes safely
app.state.engine = engine
app.state.runtime = runtime

# =========================
# Route Registration
# =========================
app.include_router(engine_router)
app.include_router(state_router)
app.include_router(config_router)
app.include_router(trading_router)
app.include_router(markers_router)

# =========================
# Health Check
# =========================
@app.get("/health")
def health_check():
    return {"status": "ok"}
