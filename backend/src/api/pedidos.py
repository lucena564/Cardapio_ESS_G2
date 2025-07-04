from fastapi import APIRouter, status
from src.schemas.response import HttpResponseModel
from src.service.impl.item_service import ItemService
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from Utils.constants import Constants
import json
import os
from datetime import datetime
import uuid

router = APIRouter()

# BaseModel é uma classe base do Pydantic que permite a criação de modelos de dados
# Ele serve para validar e serializar dados de forma fácil e eficiente
class PedidoItem(BaseModel):
    produto_id: str
    quantidade: int

class Pedido(BaseModel):
    mesa: str
    itens: List[PedidoItem]

class PedidoModificar(BaseModel):
    itens: Optional[List[PedidoItem]] = None

def ler_pedidos():
    """
        Função para ler os pedidos realizados do arquivo JSON.
        Se o arquivo não existir, cria um arquivo base com mesas e total zerado.
    """
    if not os.path.exists(Constants.PEDIDOS_FILE):
        base = {
            "mesas": ["mesa_1", "mesa_2", "mesa_3", "mesa_4", "mesa_5"],
            "mesa_1": {"pedidos": [], "total": 0},
            "mesa_2": {"pedidos": [], "total": 0},
            "mesa_3": {"pedidos": [], "total": 0},
            "mesa_4": {"pedidos": [], "total": 0},
            "mesa_5": {"pedidos": [], "total": 0},
        }
        salvar_pedidos(base)
        return base

    with open(Constants.PEDIDOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def salvar_pedidos(data):
    """
        Função para salvar os pedidos realizados no arquivo JSON.
    """
    with open(Constants.PEDIDOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ler_cardapio():
    """
        Função para ler o cardápio de produtos do arquivo JSON.
        Se o arquivo não existir, levanta uma exceção.
    """
    with open(Constants.CARDAPIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def calcular_total(itens_pedido, cardapio_produtos):
    """
        Função para calcular o total de um pedido com base nos itens e no cardápio.

        Cada item do pedido é um objeto PedidoItem com produto_id e quantidade.

        O cardápio é uma lista de dicionários com ID, PRECO e opcionalmente DESCONTO.
    """
    total = 0
    for item in itens_pedido:
        produto = next((p for p in cardapio_produtos if p["ID"] == item.produto_id), None)
        if produto:
            preco = produto["PRECO"]
            desconto = produto.get("DESCONTO", 0)
            preco_com_desconto = preco * (1 - desconto / 100)
            total += preco_com_desconto * item.quantidade
        else:
            raise HTTPException(status_code=400, detail=f"Produto ID {item.produto_id} não encontrado no cardápio")
    return round(total, 2)

# Funções para histórico de pedidos
def ler_historico() -> List[dict]:
    """
    Função para ler o histórico de pedidos do arquivo JSON.
    Se o arquivo não existir ou estiver vazio, retorna uma lista vazia.
    """
    if not os.path.exists(Constants.HISTORY_FILE) or os.path.getsize(Constants.HISTORY_FILE) == 0:
        return []
    with open(Constants.HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_historico(data: List[dict]):
    """
    Função para salvar o histórico de pedidos no arquivo JSON.
    """
    with open(Constants.HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)



# ENDPOINT 1 - GET pedidos realizados
@router.get("/", tags=["pedidos"])
def get_pedidos_realizados():
    """
        Endpoint para obter os pedidos realizados.

        metodo: GET
        caminho: localhost:8000/pedidos
        payload: 
        ```json
        {}
        ```
    """
    pedidos = ler_pedidos()
    return pedidos


# ENDPOINT 2 - POST fazer pedido
@router.post("/", status_code=status.HTTP_201_CREATED, tags=["pedidos"])
def fazer_pedido(pedido: Pedido):
    """
Endpoint para fazer um pedido em uma mesa específica.

Método: POST  
Caminho: /pedidos 

Payload:
```json
{
  "mesa": "mesa_1",
  "itens": [
    { "produto_id": "<id_de_dados.json>", "quantidade": x },
    { "produto_id": "<id_de_dados.json>", "quantidade": y },
    ...
    { "produto_id": "<id_de_dados.json>", "quantidade": z }
  ]
}
```
    """

    pedidos = ler_pedidos()
    cardapio = ler_cardapio()

    if pedido.mesa not in pedidos["mesas"]:
        raise HTTPException(status_code=400, detail="Mesa inválida")

    # Atualiza os pedidos da mesa
    mesa = pedidos[pedido.mesa]

    # Adiciona os itens do pedido na lista
    for item in pedido.itens:
        mesa["pedidos"].append({
            "produto_id": item.produto_id,
            "quantidade": item.quantidade
        })

    # Recalcula o total
    try:
        itens_pedido_obj = [PedidoItem(**item) for item in mesa["pedidos"]]
        mesa["total"] = calcular_total(itens_pedido_obj, cardapio["produtos"])
    except HTTPException as e:
        raise e

    salvar_pedidos(pedidos)
    return {"message": "Pedido realizado com sucesso", "mesa": pedido.mesa, "total": mesa["total"]}


# ENDPOINT 3 - PUT modificar pedido
@router.put("/{mesa}", tags=["pedidos"])
def modificar_pedido(mesa: str, pedido_mod: PedidoModificar):
    """
Endpoint para modificar um pedido existente em uma mesa específica.

Método: PUT  
Caminho: /pedidos/{mesa}

Payload:
```json
{
  "itens": [
    {
      "produto_id": "B002",
      "quantidade": 1
    },
    {
      "produto_id": "O001",
      "quantidade": 1
    }
  ]
}
```
    """
    pedidos = ler_pedidos()
    cardapio = ler_cardapio()

    if mesa not in pedidos["mesas"]:
        raise HTTPException(status_code=400, detail="Mesa inválida")

    if not pedidos[mesa]["pedidos"]:
        raise HTTPException(status_code=400, detail="Nenhum pedido encontrado para esta mesa, por favor, faça um pedido primeiro")

    if not pedido_mod.itens:
        raise HTTPException(status_code=400, detail="Lista de itens não pode ser vazia")

    mesa_data = pedidos[mesa]

    if pedido_mod.itens is not None:
        # Substitui os pedidos atuais pelos novos itens
        mesa_data["pedidos"] = [{"produto_id": item.produto_id, "quantidade": item.quantidade} for item in pedido_mod.itens]

        # Recalcula total
        try:
            itens_pedido_obj = [PedidoItem(**item) for item in mesa_data["pedidos"]]
            mesa_data["total"] = calcular_total(itens_pedido_obj, cardapio["produtos"])
        except HTTPException as e:
            raise e

        salvar_pedidos(pedidos)
        return {"message": "Pedido modificado com sucesso", "mesa": mesa, "total": mesa_data["total"]}

    else:
        raise HTTPException(status_code=400, detail="Nenhum dado para modificar fornecido")
    
# ENDPOINT 4 - POST fechar pedido e mover pro histórico
@router.post("/fechar/{mesa}", status_code=status.HTTP_200_OK, tags=["pedidos"])
def fechar_pedido(mesa: str):
    """
    Endpoint para fechar o pedido de uma mesa.
    O pedido é movido para o histórico e a mesa é zerada.

    Método: POST
    Caminho: /pedidos/fechar/{mesa}
    """
    pedidos_ativos = ler_pedidos()

    if mesa not in pedidos_ativos["mesas"]:
        raise HTTPException(status_code=404, detail="Mesa não encontrada.")

    mesa_data = pedidos_ativos[mesa]

    if not mesa_data["pedidos"]:
        raise HTTPException(status_code=400, detail="Não há pedido ativo para fechar nesta mesa.")

    # Carrega o histórico de pedidos existente
    historico = ler_historico()

    # Cria o novo registro para o histórico com detalhes adicionais
    pedido_finalizado = {
        "id_historico": str(uuid.uuid4()),  # Gera um ID único para o registro
        "mesa": mesa,
        "itens": mesa_data["pedidos"],
        "total": mesa_data["total"],
        "data_fechamento": datetime.now().isoformat()  # Adiciona data e hora do fechamento
    }

    # Adiciona o pedido finalizado ao histórico e salva o arquivo
    historico.append(pedido_finalizado)
    salvar_historico(historico)

    # Limpa os dados da mesa no arquivo de pedidos ativos
    pedidos_ativos[mesa]["pedidos"] = []
    pedidos_ativos[mesa]["total"] = 0
    salvar_pedidos(pedidos_ativos)

    return {"message": f"Pedido da {mesa} fechado com sucesso e movido para o histórico.", "pedido_arquivado": pedido_finalizado}