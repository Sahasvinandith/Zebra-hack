from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .consumer import process_event, get_alerts

app = FastAPI(title="Project Sentinel Engine")

@app.post("/ingest/{source}")
async def ingest(source: str, event: dict):
    alerts = process_event(source, event)
    return JSONResponse(content={"received": True, "alerts": alerts})

@app.get("/alerts")
async def alerts():
    return get_alerts()
