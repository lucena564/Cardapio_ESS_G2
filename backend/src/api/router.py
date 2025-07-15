from fastapi import APIRouter
from src.api import pedidos, cache, order_history, categorias, adm_client

api_router = APIRouter()

api_router.include_router(pedidos.router, prefix="/pedidos", tags=["pedidos"])

api_router.include_router(cache.router, prefix="/clear", tags=["pedidos"])

api_router.include_router(order_history.router, prefix="/historico", tags=["historico"])

api_router.include_router(adm_client.router, prefix="/admin", tags=["admin"])

# ENDPOINTS destinados a categorias
api_router.include_router(categorias.router, prefix="/categorias", tags=["categorias"])