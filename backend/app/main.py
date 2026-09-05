import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.database import engine, Base, SessionLocal
from app.db import models
from app.services.seeder import seed_database_if_empty
from app.api.routes import works, anomalies, assistant

# Create database tables automatically
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-seed database from verified NIDHI TRACE records if table is empty
    db = SessionLocal()
    try:
        seed_database_if_empty(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title="NIDHI TRACE API",
    description="Intelligent Public Fund Surveillance & Anomaly Detection API",
    version="2.6.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core Routers
app.include_router(works.router, prefix="/api/works", tags=["works"])
app.include_router(anomalies.router, prefix="/api/anomalies", tags=["anomalies"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["assistant"])

@app.get("/health")
def health():
    return {"status": "ok", "platform": "NIDHI TRACE", "version": "2.6.0"}

@app.get("/")
def root():
    return {
        "message": "NIDHI TRACE Central Ledger & Anomaly Detection API",
        "docs": "/docs",
        "health": "/health"
    }
