from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid
import json
import os
from Utils.constants import Constants


router = APIRouter()

# app = FastAPI(title="Cardápio Virtual - Histórico de Pedidos", version="1.0.0")

# Enums
class StatusPedido(str, Enum):
    EMANDAMENTO = "em andamento"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"

# Models
class ItemPedido(BaseModel):
    id: str
    nome: str
    quantidade: int
    preco_unitario: float
    observacoes: Optional[str] = None

class Order(BaseModel):
    idOrder: str
    numero_pedido: int  # 4 dígitos
    data: str  # formato YYYY-MM-DD
    hora: str  # formato HH:MM
    valor: float
    itens: List[ItemPedido]
    mesa: Optional[int] = None
    status: StatusPedido

class OrderCreate(BaseModel):
    itens: List[ItemPedido]
    mesa: Optional[int] = None

class OrderUpdate(BaseModel):
    status: StatusPedido


def ler_historico() -> List[dict]:
    """
    Função para ler o histórico de pedidos do arquivo JSON.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    if not os.path.exists(Constants.HISTORY_FILE):
        return []
    
    # Se o arquivo estiver vazio, evitamos um erro de JSON
    if os.path.getsize(Constants.HISTORY_FILE) == 0:
        return []

    with open(Constants.HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ENDPOINT - GET /historico
@router.get("/{mesa}", status_code=status.HTTP_200_OK, tags=["historico"])
def get_historico_pedidos(mesa: str):
    """
    Endpoint para obter o histórico de todos os pedidos já finalizados.

    Metodo: GET
    Caminho: http://localhost:8000/historico/{nome_mesa}
    Exemplo: http://localhost:8000/historico/mesa_1
    """
    historico = ler_historico()
    # Filtra a lista de histórico para encontrar apenas os pedidos da mesa especificada
    historico_da_mesa = [pedido for pedido in historico if pedido.get("mesa") == mesa]

    # Se, após filtrar, a lista estiver vazia, significa que a mesa não tem histórico
    if not historico_da_mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhum histórico encontrado para a {mesa}. Verifique se a mesa existe ou se já finalizou algum pedido."
        )

    return historico_da_mesa
