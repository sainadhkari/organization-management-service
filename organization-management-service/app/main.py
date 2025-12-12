# app/main.py
from fastapi import FastAPI
from app.org.org_controller import router as org_router

app = FastAPI(title="Organization Management Service")
app.include_router(org_router)

@app.get("/health")
def health():
    return {"status": "ok"}
