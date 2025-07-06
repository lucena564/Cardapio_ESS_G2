from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.api.router import api_router

from Utils.constants import Constants
import json
import os

# Cria o arquivo defalt do `pedidos_realizados.json` caso não exista
if not os.path.exists(Constants.PEDIDOS_FILE):

    base = Constants.PEDIDOS_REALIZADOS_DEFAULT

    with open(Constants.PEDIDOS_FILE, "w", encoding="utf-8") as f:
        json.dump(base, f, indent=2, ensure_ascii=False)

# Cria o arquivo defalt do `dados.json` caso não exista
if not os.path.exists(Constants.CARDAPIO_FILE):

    base = Constants.CARDAPIO_DEFAULT

    with open(Constants.CARDAPIO_FILE, "w", encoding="utf-8") as f:
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