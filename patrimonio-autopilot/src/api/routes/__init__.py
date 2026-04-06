from src.api.routes.portfolios import router as portfolios_router
from src.api.routes.orders import router as orders_router
from src.api.routes.auth import router as auth_router
from src.api.routes.signals import router as signals_router
from src.api.routes.autopilot import router as autopilot_router

__all__ = ["portfolios_router", "orders_router", "auth_router", "signals_router", "autopilot_router"]
