from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
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
    produto_id: str
    nome: str
    quantidade: int
    valor_unitario: float
    categoria: str

class Order(BaseModel):
    id_historico: str # 4 digitos
    mesa: str
    itens: List[ItemPedido]
    total: float
    data_fechamento: str  
    status: StatusPedido

class OrderCreate(BaseModel):
    itens: List[ItemPedido]
    mesa: Optional[int] = None

class OrderUpdate(BaseModel):
    status: StatusPedido

class DeleteRequest(BaseModel):
    ids_historico: List[str]

'''class OrderFilter(BaseModel):
    tipo: str
    valor:
'''

def ler_historico() -> List[dict]:
    """
    Função para ler o histórico de pedidos do arquivo JSON.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    if not os.path.exists(Constants.HISTORY_FILE):
        return []
    
    if os.path.getsize(Constants.HISTORY_FILE) == 0:
        return []

    with open(Constants.HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_historico(data: List[dict]):
    with open(Constants.HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

# ENDPOINT - PUT /historico
@router.put("/{id_historico}", status_code=status.HTTP_200_OK, tags=["historico"])
def put_historico_pedidos(id_historico: str, pedido_atualizado: Order):
    """
    Endpoint para atualizar o histórico 

    Metodo: PUT
    Caminho: http://localhost:8000/historico/{id_historico}
    Exemplo: http://localhost:8000/historico/0001
    Payload:
    ```json
    {
    "id_historico": "0001",
    "mesa": "mesa_1",
    "itens": [
      {
        "produto_id": "B004",
        "quantidade": 3
      }
    ],
    "total": 24.3,
    "data_fechamento": "2025-07-09T13:33:02.135748",
    "status": "Concluído"
    }
    ```
    """
    historico = ler_historico()

    # Filtra histórico pelo id do item a substituir 
    idx_pedido = -1
    for i, pedido in enumerate(historico):
        if pedido.get("id_historico") == id_historico:
            idx_pedido = i
            break
    if idx_pedido == -1:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Pedido com ID {id_historico} não encontrado no histórico."
        )
    # Converte o modelo Pydantic recebido para um dicionário
    dados_atualizados_dict = pedido_atualizado.model_dump()
    
    # Substitui o dicionário antigo pelo novo no índice encontrado
    historico[idx_pedido] = dados_atualizados_dict
    
    # Salva a lista inteira de volta no arquivo JSON
    salvar_historico(historico)
    
    # Retorna o objeto atualizado
    return dados_atualizados_dict

# ENDPOINT - DELETE /historico
@router.delete("/", status_code=status.HTTP_200_OK, tags=["historico"])
def delete_historico_pedidos(req: DeleteRequest):
    """
    Endpoint para deletar um ou mais pedidos do histórico (versão recomendada).
    
    Metodo: DELETE
    Caminho: http://localhost:8000/historico
    """
    historico_original = ler_historico()
    ids_a_remover = req.ids_historico
    
    tamanho_original = len(historico_original)
    
    historico_atualizado = [
        pedido for pedido in historico_original 
        if pedido.get("id_historico") not in ids_a_remover
    ]
    
    if len(historico_atualizado) == tamanho_original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum dos IDs fornecidos foi encontrado no histórico."
        )

    salvar_historico(historico_atualizado)
    
    return {"message": "Pedidos selecionados foram removidos com sucesso."}

@router.get("{mesa}/filtrar", tags=["historico"], response_model=List[Order]) 
def filtrar_historico(
    mesa: str,
    nome_item: Optional[str] = Query(None, description="Filtrar por nome parcial do item."),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria exata do item."),
    data: Optional[str] = Query(None, description="Filtrar por data no formato YYYY-MM-DD."),
    status: Optional[str] = Query(None, description="Filtrar por status ('concluido', 'cancelado', 'em andamento').")
):
    """
    Endpoint para obter o histórico filtrado.

    Metodo: GET
    Caminho: http://localhost:8000/historico/{nome_mesa}/filtrar
    Exemplo: http://localhost:8000/historico/mesa_1/filtrar
    """
    historico = ler_historico()
    historico_da_mesa = [pedido for pedido in historico if pedido.get("mesa") == mesa]


    # Filtra a lista de histórico para encontrar apenas os pedidos da mesa especificada
    if status:
        # Mantém na lista apenas os pedidos cujo status corresponde ao filtro (ignorando maiúsculas/minúsculas)
        historico_da_mesa = [p for p in historico_da_mesa if p.get('status', '').lower() == status.lower()]

    # Filtro por DATA
    if data:
        # Mantém apenas os pedidos cuja data de fechamento começa com a data fornecida
        historico_da_mesa = [p for p in historico_da_mesa if p.get('data_fechamento', '').startswith(data)]

    # Filtro por NOME DO ITEM
    if nome_item:
        pedidos_filtrados = []
        for pedido in historico_da_mesa:
            # Verifica se QUALQUER item dentro do pedido contém o nome pesquisado
            if any(nome_item.lower() in item.get('nome', '').lower() for item in pedido.get('itens', [])):
                pedidos_filtrados.append(pedido)
        historico_da_mesa = pedidos_filtrados

    # Filtro por CATEGORIA
    if categoria:
        pedidos_filtrados = []
        for pedido in historico_da_mesa:
            # Verifica se QUALQUER item dentro do pedido pertence à categoria pesquisada
            if any(item.get('categoria', '').lower() == categoria.lower() for item in pedido.get('itens', [])):
                pedidos_filtrados.append(pedido)
        historico_da_mesa = pedidos_filtrados

    return historico_da_mesa