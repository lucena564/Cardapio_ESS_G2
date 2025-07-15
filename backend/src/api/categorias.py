from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status
from Utils.categorias_utils import ler_categorias, salvar_categorias
# Importando as funções utilitárias para manipulação de categorias
router = APIRouter()

class Categorias(BaseModel):
    categoria: str

# ENDPOINT 1 - GET listar categorias
@router.get("/", status_code=status.HTTP_200_OK, tags=["categorias"])
def listar_categorias():
    """
        Endpoint para obter a lista de categorias disponíveis.

        método: GET
        caminho: localhost:8000/categorias
        payload:
        ```json
        {}
        ```
        resposta:
        ```json
        ["BEBIDAS", "LANCHES", ...]
        ```
    """
    return ler_categorias()

# ENDPOINT 2 - POST criar categoria
@router.post("/", status_code=status.HTTP_201_CREATED, tags=["categorias"])
def criar_categoria(nome: Categorias):
    """
        Endpoint para criar uma nova categoria.

        método: POST
        caminho: localhost:8000/categorias
        payload:
        ```json
        {
            "categoria": "NOME_DA_CATEGORIA"
        }
        ```
        resposta (sucesso):
        ```json
        {
            "mensagem": "Categoria criada",
            "nome": "NOME_DA_CATEGORIA"
        }
        ```
    """
    nome = nome.categoria
    
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
        Endpoint para atualizar o nome de uma categoria existente.

        método: PUT
        caminho: localhost:8000/categorias/{nome_antigo}
        payload:
        ```json
        {
            "categoria": "NOVO_NOME"
        }
        ```
        resposta (sucesso):
        ```json
        {
            "mensagem": "Categoria atualizada",
            "nome": "NOVO_NOME"
        }
        ```
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
        Endpoint para remover uma categoria existente.

        método: DELETE
        caminho: localhost:8000/categorias/{nome}
        payload:
        ```json
        {}
        ```
        resposta (sucesso):
        ```json
        {
            "mensagem": "Categoria removida"
        }
        ```
    """
    categorias = ler_categorias()
    
    if nome not in categorias:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    categorias.remove(nome)
    
    salvar_categorias(categorias)
    
    return {"mensagem": "Categoria removida"}