# src/api/sugestoes.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Set, Optional
import json
import os

# Importa as funções de leitura do arquivo pedidos.py
from src.api.pedidos import ler_cardapio, ler_pedidos
from Utils.constants import Constants # Importa Constants para os caminhos dos arquivos

router = APIRouter()

# Classes

class ItemSugerido(BaseModel):
    id: str
    nome: str
    descricao: str
    preco: float
    categoria: str

class ProdutoSugestao(BaseModel):
    produto_id: str

class Sugestao(BaseModel):
    nome: str
    items: List[ProdutoSugestao]

class NovaSugestao(BaseModel):
    nome: str
    combinacao: List[ProdutoSugestao]


def ler_regras_sugestao() -> Dict:
    """
    Lê as regras de sugestão do arquivo JSON.
    Se o arquivo não existir, cria um base no novo formato:
    {
        "nomes_sugestao": ["Rulenome1", "Rulenome2"],
        "nome_sugestao": {"items": [{"produto_id": "P1"}, {"produto_id": "P2"}]},
        "nome_sugestao": {"items": [{"produto_id": "P3"}, {"produto_id": "P4"}]},
        ...
    }
    """
    if not os.path.exists(Constants.SUGESTOES_FILE):
        base_rules = {"nomes_sugestao": []}
        salvar_regras_sugestao(base_rules)
        return base_rules
    with open(Constants.SUGESTOES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_regras_sugestao(data: Dict):
    """Salva as regras de sugestão no arquivo JSON."""
    with open(Constants.SUGESTOES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_product_details(produto_id: str, cardapio_produtos: List[Dict]) -> Optional[Dict]:
    """Retorna os detalhes de um produto a partir do ID do cardápio."""
    return next((p for p in cardapio_produtos if p["ID"] == produto_id), None)

# Filtragem de Sugestoes

def obter_sugestoes_para_carrinho( 
    items_carrinho: List[Dict], 
    produtos_cardapio: List[Dict] 
) -> List[ItemSugerido]:
    """
    Gera sugestões de items baseadas nos items do carrinho, focando apenas na presença/ausência.
    """
    dados_sugestoes = ler_regras_sugestao() 
    dicionario_regras_sugestao = {chave: valor for chave, valor in dados_sugestoes.items() if chave != "nomes_sugestao"}
    lista_regras_sugestao = [detalhes_regra for detalhes_regra in dicionario_regras_sugestao.values()] 

    ids_produtos_carrinho = {item["produto_id"] for item in items_carrinho}

    ids_produtos_sugeridos_finais: Set[str] = set() 

    for regra in lista_regras_sugestao: 
        ids_produtos_regra = {item["produto_id"] for item in regra["items"]} 

        # Seleciona produtos que estao no carrinho e na sugestao
        produtos_comuns = ids_produtos_carrinho.intersection(ids_produtos_regra) 

        # Ao encontrar produtos em comum, seleciona agora os que faltaram da sugestao, se houver
        if produtos_comuns:
            produtos_faltando_na_regra = ids_produtos_regra.difference(ids_produtos_carrinho) 

            for id_produto_a_sugerir in produtos_faltando_na_regra: 
                ids_produtos_sugeridos_finais.add(id_produto_a_sugerir)

    lista_sugestoes: List[ItemSugerido] = [] 
    for id_item in ids_produtos_sugeridos_finais: 
        detalhes_produto = get_product_details(id_item, produtos_cardapio) 
        if detalhes_produto:
            lista_sugestoes.append(ItemSugerido(
                id=detalhes_produto["ID"],
                nome=detalhes_produto["NOME"],
                descricao=detalhes_produto["DESCRICAO"],
                preco=detalhes_produto["PRECO"],
                categoria=detalhes_produto["CATEGORIA"]
            ))
    return lista_sugestoes


# ENDPOINT 1 - GET tuplas de sugestoes
@router.get("/regras", response_model=List[Sugestao], tags=["sugestoes_admin"])
def get_all_suggestion_rules():
    """
    Retorna todas as regras de sugestão cadastradas no sistema.
    """
    sugestoes_data = ler_regras_sugestao()
    conjunto_sugestoes = []
    for sugestao_nome in sugestoes_data.get("nomes_sugestao", []):
        rule_details = sugestoes_data.get(sugestao_nome)
        if rule_details:
            conjunto_sugestoes.append(Sugestao(nome=sugestao_nome, items=[ProdutoSugestao(produto_id=item["produto_id"]) for item in rule_details["items"]]))
    return conjunto_sugestoes

# ENDPOINT 2 - POST nova tupla de sugestao
@router.post("/regras", status_code=status.HTTP_201_CREATED, tags=["sugestoes_admin"])
def adicionar_regra_sugestao(payload_nova_regra: NovaSugestao): # Renomeado de 'add_suggestion_rule', 'new_rule_payload'
    """
    Adiciona uma nova regra de sugestão de items.
    Exemplo de payload: {"nome": "Novo Combo", "combinacao": [{"produto_id": "L001"}, {"produto_id": "A001"}]}
    """
    dados_sugestoes = ler_regras_sugestao() # Renomeado de 'sugestoes_data'
    dados_cardapio = ler_cardapio() # Renomeado de 'cardapio_data'
    ids_produtos_existentes = {p["ID"] for p in dados_cardapio["produtos"]} # Renomeado de 'existing_produto_ids'

    # Valida IDs de produtos na nova regra
    for item in payload_nova_regra.combinacao: # Renomeado de 'item'
        if item.produto_id not in ids_produtos_existentes:
            raise HTTPException(status_code=400, detail=f"Produto ID '{item.produto_id}' na combinação não encontrado no cardápio.")

    # Garante nome único
    if payload_nova_regra.nome in dados_sugestoes:
        raise HTTPException(status_code=409, detail=f"Regra com o nome '{payload_nova_regra.nome}' já existe. Nomes de regras devem ser únicos.")

    # Considerando apenas IDs de produtos
    conjunto_ids_produtos_nova_regra = frozenset(item.produto_id for item in payload_nova_regra.combinacao) # Renomeado de 'new_rule_produto_ids_set'

    for nome_regra_existente in dados_sugestoes.get("nomes_sugestao", []): # Renomeado de 'existing_sugestao_nome'
        detalhes_regra_existente = dados_sugestoes.get(nome_regra_existente) # Renomeado de 'existing_rule_details'
        if detalhes_regra_existente:
            conjunto_ids_produtos_regra_existente = frozenset(item["produto_id"] for item in detalhes_regra_existente["items"]) # Renomeado de 'existing_rule_produto_ids_set'
            if conjunto_ids_produtos_nova_regra == conjunto_ids_produtos_regra_existente:
                raise HTTPException(status_code=409, detail="Combinação de produtos idêntica (mesmos IDs de produtos) já existe, mesmo com nome diferente.")

    
    dados_sugestoes[payload_nova_regra.nome] = {
        # Armazena apenas id_produto para cada item na combinação
        "items": [{"produto_id": item.produto_id} for item in payload_nova_regra.combinacao]
    }
    
    dados_sugestoes["nomes_sugestao"].append(payload_nova_regra.nome)

    salvar_regras_sugestao(dados_sugestoes)
    return {"message": "Regra de sugestão adicionada com sucesso", "nome_regra_adicionada": payload_nova_regra.nome} # Renomeado de 'rule_added_nome'

# ENDPOINT 3 - DELETE tupla de sugestao
@router.delete("/regras/{sugestao_nome}", status_code=status.HTTP_200_OK, tags=["sugestoes_admin"])
def delete_suggestion_rule(sugestao_nome: str):
    """
    Deleta uma regra de sugestão de items pelo seu nome único.
    O nome da regra a ser deletada deve ser fornecido no path.
    """
    sugestoes_data = ler_regras_sugestao()

    if sugestao_nome not in sugestoes_data:
        raise HTTPException(status_code=404, detail=f"Regra de sugestão com o nome '{sugestao_nome}' não encontrada.")

    del sugestoes_data[sugestao_nome]
    sugestoes_data["nomes_sugestao"].remove(sugestao_nome)

    salvar_regras_sugestao(sugestoes_data)
    return {"message": f"Regra de sugestão '{sugestao_nome}' deletada com sucesso", "remaining_rules_count": len(sugestoes_data["nomes_sugestao"])}


# ENDPOINT 1 - GET sugestoes de uma mesa
@router.get("/{mesa}", response_model=List[ItemSugerido], tags=["sugestoes"])
def get_sugestoes_mesa(mesa: str):
    """
    Retorna sugestões de items para uma mesa específica, baseadas nos items
    atualmente em seu pedido e nas regras de sugestão (apenas presença).
    """
    pedidos_data = ler_pedidos()
    cardapio_data = ler_cardapio()

    if mesa not in pedidos_data["mesas"]:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")

    mesa_pedidos = pedidos_data[mesa]["pedidos"]
    if not mesa_pedidos:
        return []

    sugestoes = obter_sugestoes_para_carrinho(mesa_pedidos, cardapio_data["produtos"])
    return sugestoes