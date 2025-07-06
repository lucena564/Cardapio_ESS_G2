from fastapi import APIRouter
from src.api import pedidos, cache, items
from src.api.adm_client import router as adm_client_router

# Esse import era o exemplo do banco que veio junto à configuração do projeto.
# from src.api import items

api_router = APIRouter()

# Esse é o router exemplo do banco que veio junto à configuração do projeto.
# api_router.include_router(items.router, prefix="/items", tags=["items"])

api_router.include_router(pedidos.router, prefix="/pedidos", tags=["pedidos"])

api_router.include_router(cache.router, prefix="/clear", tags=["pedidos"])

api_router.include_router(adm_client_router, prefix="/admin", tags=["admin"])