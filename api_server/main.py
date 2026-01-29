# api_server/main.py

from fastapi import FastAPI

app = FastAPI(title="SmartTradeX API", version="1.0")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SmartTradeX API running"}