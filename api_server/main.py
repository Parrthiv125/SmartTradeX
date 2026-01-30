from fastapi import FastAPI
from api_server.routes.state import router as state_router
from api_server.routes.config import router as config_router
from api_server.routes.engine import router as engine_router


app = FastAPI(title="SmartTradeX API", version="1.0")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SmartTradeX API running"}

app.include_router(state_router)
app.include_router(config_router)
app.include_router(engine_router)
