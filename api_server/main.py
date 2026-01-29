from fastapi import FastAPI
from api_server.routes.state import router as state_router

app = FastAPI(title="SmartTradeX API", version="1.0")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SmartTradeX API running"}

# attach state routes
app.include_router(state_router)