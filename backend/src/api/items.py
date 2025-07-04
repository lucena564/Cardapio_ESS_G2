from fastapi import APIRouter, HTTPException
from typing import List
import uuid

# As importações devem vir dos seus módulos locais
from src.schemas.item import Produto, ProdutoCreate, ProdutoUpdate
from src.db.database import carregar_db, salvar_db

# Criação do Router
router = APIRouter()

# Rota POST para criar item (que você já tem)
@router.post("/", response_model=Produto, status_code=201)
def criar_item(item_create: ProdutoCreate):
    """Cria um novo item no cardápio."""
    db_data = carregar_db()
    novo_item = item_create.model_dump()
    novo_item["ID"] = str(uuid.uuid4())

    db_data["produtos"].append(novo_item)
    salvar_db(db_data)
    return novo_item

# Rota GET para listar itens (que você já tem)
@router.get("/", response_model=List[Produto])
def listar_items():
    """Lista todos os itens do cardápio."""
    db_data = carregar_db()
    return db_data["produtos"]

# --- CÓDIGO NOVO ADICIONADO ABAIXO ---

# Rota PUT para ATUALIZAR um item (e gerenciar promoções)
@router.put("/{item_id}", response_model=Produto)
def atualizar_item(item_id: str, produto_update: ProdutoUpdate):
    """
    Atualiza um produto existente usando seu ID.
    Esta rota é usada para editar qualquer informação do item,
    incluindo adicionar ou modificar um DESCONTO para torná-lo promocional.
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

# Rota DELETE para REMOVER um item
@router.delete("/{item_id}", status_code=204)
def remover_item(item_id: str):
    """Remove um produto do cardápio usando o seu ID."""
    db_data = carregar_db()
    produto_para_remover = next((p for p in db_data['produtos'] if p['ID'] == item_id), None)
    
    if not produto_para_remover:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    db_data['produtos'].remove(produto_para_remover)
    salvar_db(db_data)
    
    return