from src.api.routes.portfolios import router as portfolios_router
from src.api.routes.orders import router as orders_router
from src.api.routes.auth import router as auth_router

__all__ = ["portfolios_router", "orders_router", "auth_router"]
