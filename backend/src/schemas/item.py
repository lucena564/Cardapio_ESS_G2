from typing import Optional
from pydantic import BaseModel

class ProdutoCreate(BaseModel):
    NOME: str
    DESCRICAO: str
    PRECO: float
    DESCONTO: int = 0
    CATEGORIA: str

class Produto(ProdutoCreate):
    ID: str

class ProdutoUpdate(BaseModel):
    NOME: Optional[str] = None
    DESCRICAO: Optional[str] = None
    PRECO: Optional[float] = None
    DESCONTO: Optional[int] = None
    CATEGORIA: Optional[str] = None