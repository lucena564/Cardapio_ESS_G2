from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status
from Utils.categorias_utils import ler_categorias, salvar_categorias
# Importando as funções utilitárias para manipulação de categorias
router = APIRouter()

class Categorias(BaseModel):
    categoria: str

# ENDPOINT 1 - GET listar categorias
@router.get("/", tags=["categorias"])
def listar_categorias():
    """
    Retorna a lista de categorias disponíveis.
    
    """
    return ler_categorias()

# ENDPOINT 2 - POST criar categoria
@router.post("/", status_code=status.HTTP_201_CREATED, tags=["categorias"])
def criar_categoria(nome: Categorias):
    """
    
    Cria uma nova categoria se ela não existir e o nome for válido.
    
    """
    nome = nome.categoria
    
    # Verifica se o nome da categoria é válido
    if not nome or not nome.strip():
        raise HTTPException(status_code=400, detail="O nome da categoria é obrigatório")
    
    categorias = ler_categorias()
    
    if nome in categorias:
        raise HTTPException(status_code=400, detail="Categoria já existe")
    
    categorias.append(nome)
    
    salvar_categorias(categorias)
    
    return {"mensagem": "Categoria criada", "nome": nome}

# ENDPOINT 3 - PUT atualizar categoria
@router.put("/{nome_antigo}", status_code=status.HTTP_200_OK, tags=["categorias"])
def atualizar_categoria(nome_antigo: str, nome_novo: Categorias):
    """
    
    Atualiza o nome de uma categoria existente.
    
    """
    categorias = ler_categorias()
    
    if nome_antigo not in categorias:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    if nome_novo.categoria in categorias:
        raise HTTPException(status_code=400, detail="Nova categoria já existe")
    
    categorias[categorias.index(nome_antigo)] = nome_novo.categoria
    
    salvar_categorias(categorias)

    return {"mensagem": "Categoria atualizada", "nome": nome_novo.categoria}

# ENDPOINT 4 - DELETE deletar categoria
@router.delete("/{nome}", status_code=status.HTTP_200_OK, tags=["categorias"])
def deletar_categoria(nome: str):
    """
    Remove uma categoria existente.
    
    """
    categorias = ler_categorias()
    
    if nome not in categorias:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    categorias.remove(nome)
    
    salvar_categorias(categorias)
    
    return {"mensagem": "Categoria removida"}