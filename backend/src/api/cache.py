from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from Utils.constants import Constants
import os

router = APIRouter()

# ENDPOINT 1 - DELETE apagar todos os pedidos (remover o arquivo JSON)
@router.delete("/pedidos", status_code=status.HTTP_200_OK, tags=["pedidos"])
def resetar_pedidos():
    """
    Endpoint para apagar completamente os pedidos realizados.

    método: DELETE
    caminho: localhost:8000/clear/pedidos

    Esse método vai deletar o arquivo pedidos_realizados.json; 
    Para cria-lo novamente, basta enviar o listar pedidos ou subir a API novamente.
    """
    if os.path.exists(Constants.PEDIDOS_FILE):
        os.remove(Constants.PEDIDOS_FILE)
        return {"message": "Arquivo de pedidos apagado com sucesso"}
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Arquivo de pedidos não encontrado."}
        )