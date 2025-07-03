from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.api.router import api_router

from Utils.constants import Constants
import json
import os

if not os.path.exists(Constants.PEDIDOS_FILE):
    base = {
        "mesas": ["mesa_1", "mesa_2", "mesa_3", "mesa_4", "mesa_5"],
        "mesa_1": {"pedidos": [], "total": 0},
        "mesa_2": {"pedidos": [], "total": 0},
        "mesa_3": {"pedidos": [], "total": 0},
        "mesa_4": {"pedidos": [], "total": 0},
        "mesa_5": {"pedidos": [], "total": 0}
    }
    with open(Constants.PEDIDOS_FILE, "w", encoding="utf-8") as f:
        json.dump(base, f, indent=2, ensure_ascii=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)