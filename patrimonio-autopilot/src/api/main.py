import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import auth_router, orders_router, portfolios_router
from src.data import init_db


app = FastAPI(
    title="patrimonio-autopilot API",
    version="0.1.0",
    description="Base API para gestión de patrimonio y operaciones de inversión.",
)

raw_origins = os.environ.get("AUTOPILOT_CORS_ORIGINS", "http://localhost:3420,http://127.0.0.1:3420")
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "patrimonio-autopilot", "status": "ok"}


app.include_router(portfolios_router)
app.include_router(orders_router)
app.include_router(auth_router)

