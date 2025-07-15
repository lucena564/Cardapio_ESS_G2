import json
from .constants import Constants

def ler_categorias():
    """
    
    Lê a lista de categorias do arquivo dados.json.
    Retorna uma lista de strings.
    
    """
    with open(Constants.CARDAPIO_FILE, encoding="utf-8") as f:
        dados = json.load(f)
    return dados.get("categorias", [])

def salvar_categorias(categorias):
    """
    
    Salva a lista de categorias no arquivo dados.json.
    
    """
    with open(Constants.CARDAPIO_FILE, encoding="utf-8") as f:
        dados = json.load(f)
    
    dados["categorias"] = categorias
    
    with open(Constants.CARDAPIO_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)