from fastapi import FastAPI

# =========================
# API Routes
# =========================
from api_server.routes import engine as engine_routes
from api_server.routes import state as state_routes
from api_server.routes import trading as trading_routes
from api_server.routes import markers as markers_routes
from api_server.routes import config as config_routes
from api_server.routes import market as market_routes
from api_server.routes import analytics as analytics_routes


# =========================
# FastAPI App
# =========================
app = FastAPI(title="SmartTradeX API")


# =========================
# MOCK ENGINE (TEMPORARY)
# =========================
class MockEngine:
    def status(self):
        return "stopped"

    def is_running(self):
        return False


class MockRuntime:
    def start(self):
        pass

    def stop(self):
        pass


app.state.engine = MockEngine()
app.state.runtime = MockRuntime()


# =========================
# Route Registration
# =========================
app.include_router(engine_routes.router)
app.include_router(state_routes.router)
app.include_router(config_routes.router)
app.include_router(trading_routes.router)
app.include_router(markers_routes.router)
app.include_router(market_routes.router)

# NEW ANALYTICS ROUTES
app.include_router(analytics_routes.router)


# =========================
# Health Check
# =========================
@app.get("/health")
def health_check():
    return {"status": "ok", "engine": "mock"}
