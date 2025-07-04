import json
from typing import Dict, List, Any

DB_FILE = "src/db/dados.json"

def carregar_db() -> Dict[str, Any]:
    """Carrega o banco de dados do arquivo JSON."""
    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"produtos": []}
    
def salvar_db(data: Dict[str, List[Dict[str, Any]]]):
    """Salva o banco de dados no arquivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    