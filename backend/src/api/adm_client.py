# Arquivo: src/api/adm_client.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import uuid

# 1. Modelos de Dados
class ProdutoUpdate(BaseModel):
    NOME: Optional[str] = None
    DESCRICAO: Optional[str] = None
    PRECO: Optional[float] = None
    DESCONTO: Optional[int] = None
    CATEGORIA: Optional[str] = None

class ProdutoCreate(BaseModel):
    NOME: str
    DESCRICAO: str
    PRECO: float
    DESCONTO: int = 0
    CATEGORIA: str

class Produto(ProdutoCreate):
    ID: str

# TODO: Colocar usar o arquivo constants.py, importando a classe Constants para modularizar, essa constante já está mapeada lá.
# 2. Lógica de Acesso ao Banco de Dados
DB_FILE = "data/dados.json" # O caminho para o seu arquivo JSON

def carregar_db() -> Dict[str, List[Dict[str, Any]]]:
    """Lê o arquivo JSON e retorna seu conteúdo."""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver vazio, começa com uma estrutura limpa
        return {"produtos": [], "categorias": []}

def salvar_db(data: Dict[str, List[Dict[str, Any]]]):
    """Salva os dados de volta no arquivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# 3. Definição do Router e Rotas da API
# O router e todas as suas rotas de admin para gerenciar itens.
router = APIRouter()

@router.post("/items/", response_model=Produto, status_code=201, summary="Criar um novo item")
def criar_item(item_create: ProdutoCreate):
    """
    Cria um novo item no cardápio.
    Recebe os dados do produto e retorna o produto criado com um novo ID único.
    """
    db_data = carregar_db()
    novo_item = item_create.model_dump()
    novo_item["ID"] = str(uuid.uuid4())

    db_data["produtos"].append(novo_item)
    salvar_db(db_data)
    return novo_item

@router.get("/items/", response_model=List[Produto], summary="Listar todos os itens")
def listar_items():
    """Retorna uma lista de todos os produtos cadastrados no cardápio."""
    db_data = carregar_db()
    return db_data["produtos"]

@router.put("/items/{item_id}", response_model=Produto, summary="Atualizar um item")
def atualizar_item(item_id: str, produto_update: ProdutoUpdate):
    """
    Atualiza um produto existente usando seu ID.
    Esta rota é usada para editar qualquer informação do item,
    incluindo adicionar/modificar um DESCONTO para torná-lo promocional.
    """
    db_data = carregar_db()
    index_produto = next((i for i, p in enumerate(db_data['produtos']) if p['ID'] == item_id), None)

    if index_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    update_data = produto_update.model_dump(exclude_unset=True)
    produto_original = db_data['produtos'][index_produto]
    produto_atualizado = produto_original.copy()
    produto_atualizado.update(update_data)

    db_data['produtos'][index_produto] = produto_atualizado
    salvar_db(db_data)
    return produto_atualizado

@router.delete("/items/{item_id}", status_code=204, summary="Remover um item")
def remover_item(item_id: str):
    """Remove um produto do cardápio usando o seu ID."""
    db_data = carregar_db()
    produto_para_remover = next((p for p in db_data['produtos'] if p['ID'] == item_id), None)

    if not produto_para_remover:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    db_data['produtos'].remove(produto_para_remover)
    salvar_db(db_data)
    return
