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

def ler_pedidos(caminho_pedidos: str = Constants.PEDIDOS_FILE):
    """
        Função para ler os pedidos realizados do arquivo JSON.
        Se o arquivo não existir, cria um arquivo base com mesas e total zerado.
    """
    if not os.path.exists(caminho_pedidos):
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

    with open(caminho_pedidos, "r", encoding="utf-8") as f:
        return json.load(f)
    
def salvar_pedidos(data, caminho_pedidos: str = Constants.PEDIDOS_FILE):
    """
        Função para salvar os pedidos realizados no arquivo JSON.
    """
    with open(caminho_pedidos, "w", encoding="utf-8") as f:
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
def ler_historico(caminho_historico: str = Constants.HISTORY_FILE) -> List[dict]:
    """
    Função para ler o histórico de pedidos do arquivo JSON.
    Se o arquivo não existir ou estiver vazio, retorna uma lista vazia.
    """
    if not os.path.exists(caminho_historico) or os.path.getsize(caminho_historico) == 0:
        return []
    with open(caminho_historico, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_historico(data: List[dict], caminho_historico: str = Constants.HISTORY_FILE):
    """
    Função para salvar o histórico de pedidos no arquivo JSON.
    """
    with open(caminho_historico, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)



# ENDPOINT 1 - GET pedidos realizados
@router.get("/", status_code=status.HTTP_200_OK, tags=["pedidos"])
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
@router.put("/{mesa}", status_code=status.HTTP_200_OK, tags=["pedidos"])
def modificar_pedido(mesa: str, pedido_mod: PedidoModificar):
    """
    Endpoint para modificar um pedido existente em uma mesa específica.

    Método: PUT  
    Caminho: /pedidos/{mesa}

    Este endpoint permite substituir todos os itens de um pedido já existente.  
    Se a lista de itens enviada for vazia, o pedido será considerado como cancelado.

    Payload:
    ```json
    {
        "itens": [
            {
                "produto_id": "<id_do_produto>",
                "quantidade": <int quantidade dese produto>
            },
            {
                "produto_id": "<id_do_produto>",
                "quantidade": <int quantidade dese produto>
            }
        ]
    }
    ```
    Ou para cancelar o pedido:
    ```json
    {
        "itens": []
    }
    ```
    """
    pedidos = ler_pedidos()
    cardapio = ler_cardapio()

    if mesa not in pedidos["mesas"]:
        raise HTTPException(status_code=400, detail="Mesa inválida")

    if not pedidos[mesa]["pedidos"]:
        raise HTTPException(status_code=400, detail="Nenhum pedido encontrado para esta mesa, por favor, faça um pedido primeiro")

    mesa_data = pedidos[mesa] 

    if pedido_mod.itens is not None:
        # Permitir itens vazios como forma de cancelamento
        if len(pedido_mod.itens) == 0:
            mesa_data["pedidos"] = []
        else:
            mesa_data["pedidos"] = [
                {"produto_id": item.produto_id, "quantidade": item.quantidade}
                for item in pedido_mod.itens
            ]

        try:
            itens_pedido_obj = [PedidoItem(**item) for item in mesa_data["pedidos"]]
            mesa_data["total"] = calcular_total(itens_pedido_obj, cardapio["produtos"])
        except HTTPException as e:
            raise e

        salvar_pedidos(pedidos)
        return {
            "message": "Pedido modificado com sucesso",
            "mesa": mesa,
            "total": mesa_data["total"]
        }

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

    novo_id_numerico = 1
    if historico: # Verifica se a lista de histórico não está vazia
        # Pega o ID do último item, converte para inteiro e soma 1
        ultimo_id = int(historico[-1]['id_historico'])
        novo_id_numerico = ultimo_id + 1
    id_final_formatado = f"{novo_id_numerico:04d}"

    # Cria o novo registro para o histórico com detalhes adicionais
    pedido = {
        "id_historico": id_final_formatado,  # Gera um ID único para o registro
        "mesa": mesa,
        "itens": mesa_data["pedidos"],
        "total": mesa_data["total"],
        "data_fechamento": datetime.now().isoformat(),
        "status": "em andamento"
    }
    pedido_finalizado = expandir_detalhes_pedido(pedido)  # Expande os detalhes dos itens

    # Adiciona o pedido finalizado ao histórico e salva o arquivo
    historico.append(pedido_finalizado)
    salvar_historico(historico)

    # Limpa os dados da mesa no arquivo de pedidos ativos
    pedidos_ativos[mesa]["pedidos"] = []
    pedidos_ativos[mesa]["total"] = 0
    salvar_pedidos(pedidos_ativos)

    return {"message": f"Pedido da {mesa} fechado com sucesso e movido para o histórico.", "pedido_arquivado": pedido_finalizado}

# Função auxiliar para envio do json com todas informações necessárias para o historico
def expandir_detalhes_pedido(pedido_historico):
    """
    Recebe um pedido do histórico e retorna o pedido com os detalhes de cada item expandidos.
    """
    # Cria um mapa de produtos
    dados = ler_cardapio()
    mapa_produtos = {produto["ID"]: produto for produto in dados.get("produtos")}

    itens_expandidos = []
    for item_simples in pedido_historico.get("itens", []):
        produto_id = item_simples.get("produto_id")
        produto_detalhes = mapa_produtos.get(produto_id)

        if produto_detalhes:
            # Encontrou o produto, cria o item detalhado
            item_expandido = {
                "produto_id": produto_id,
                "nome": produto_detalhes.get("NOME"), 
                "quantidade": item_simples.get("quantidade"),
                "valor_unitario": produto_detalhes.get("PRECO"),
                "categoria": produto_detalhes.get("CATEGORIA")
            }
            itens_expandidos.append(item_expandido)
        else:
            # Lida com o caso de um produto não ser encontrado no cardápio
            item_expandido = {
                "produto_id": produto_id,
                "nome": "Produto não encontrado",
                "quantidade": 0,
                "valor_unitario": 0,
                "categoria": "inexistente"
            }
            itens_expandidos.append(item_expandido)

    pedido_expandido = pedido_historico.copy()
    pedido_expandido["itens"] = itens_expandidos

    return pedido_expandido