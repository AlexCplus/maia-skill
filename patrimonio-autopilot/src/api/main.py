from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import auth_router, orders_router, portfolios_router, signals_router, autopilot_router
from src.autopilot.runner import stop_all_jobs
from src.data import init_db


app = FastAPI(
    title="patrimonio-autopilot API",
    version="0.1.0",
    description="Base API para gestión de patrimonio y operaciones de inversión.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.on_event("shutdown")
def on_shutdown() -> None:
    stop_all_jobs()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "patrimonio-autopilot", "status": "ok"}


app.include_router(portfolios_router)
app.include_router(orders_router)
app.include_router(auth_router)
app.include_router(signals_router)
app.include_router(autopilot_router)

