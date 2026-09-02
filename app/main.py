import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import items

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Starter API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router, prefix="/api/v1")

BASE_DIR = Path(__file__).resolve().parent.parent

@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(BASE_DIR / "static" / "index.html")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "version": "1.0.0"}