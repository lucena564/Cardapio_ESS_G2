from fastapi import APIRouter
from src.api.items import router as items_router

api_router = APIRouter()
api_router.include_router(items_router, prefix="/items", tags=["items"])