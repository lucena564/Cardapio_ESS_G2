import json
import os
from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then, parsers
from src.main import app
from Utils.constants import Constants

client = TestClient(app)

# Caminhos para os arquivos de dados que serão manipulados
PEDIDOS_FILE_PATH = Constants.PEDIDOS_FILE
SUGESTOES_FILE_PATH = Constants.SUGESTOES_FILE
CARDAPIO_FILE_PATH = Constants.CARDAPIO_FILE 



@scenario(
    "../features/sugestao_mesa.feature",
    "Identificando itens sugeridos de uma mesa"
)
def test_identificar_sugestoes_para_mesa():
    pass

@given(parsers.cfparse('estou logado como cliente da "{mesa}"'), target_fixture="context")
def context_mesa(mesa):
    """Inicializa o contexto com o nome da mesa."""
    # Garante que os diretórios de dados existam antes de manipular os arquivos
    os.makedirs(os.path.dirname(PEDIDOS_FILE_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(SUGESTOES_FILE_PATH), exist_ok=True)
    return {"mesa": mesa}

@given(parsers.cfparse('tenho apenas o item "{produto_id}" com quantidade {quantidade:d} no carrinho'))
def preparar_carrinho_da_mesa(produto_id, quantidade):
    """
    Prepara o arquivo `pedidos.json` para simular um carrinho
    com um item específico para a mesa_1.
    """
    # Lê o cardápio para calcular o total corretamente
    with open(CARDAPIO_FILE_PATH, "r", encoding="utf-8") as f:
        cardapio_data = json.load(f)
    
    produto_info = next((p for p in cardapio_data["produtos"] if p["ID"] == produto_id), None)
    assert produto_info is not None, f"Produto {produto_id} não encontrado em dados.json"

    preco_final = produto_info["PRECO"] * (1 - produto_info.get("DESCONTO", 0) / 100)
    total_pedido = round(preco_final * quantidade, 2)
    
    pedidos_exemplo = {
        "mesas": ["mesa_1"],
        "mesa_1": {
            "pedidos": [{"produto_id": produto_id, "quantidade": quantidade}],
            "total": total_pedido
        }
    }
    with open(PEDIDOS_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(pedidos_exemplo, f, indent=2)


@given(parsers.cfparse('apenas esta cadastrada a sugestao "{nome_sugestao}" de items "{item1}" e "{item2}"'))
def preparar_regras_de_sugestao(nome_sugestao, item1, item2):
    """
    Garante que apenas a sugestão desejada esteja cadastrada no sistema.
    Remove todas as outras sugestões existentes e cria a nova via API.
    """
    # 1. Obtém todas as sugestões atuais
    response_get = client.get("/sugestoes/regras")
    assert response_get.status_code == 200
    regras_atuais = response_get.json()

    # 2. Remove todas as sugestões existentes
    for regra in regras_atuais:
        nome = regra["nome"]
        client.delete(f"/sugestoes/regras/{nome}")  # Ignora erro se já não existir

    # 3. Adiciona a sugestão necessária para o teste
    payload = {
        "nome": nome_sugestao,
        "combinacao": [
            {"produto_id": item1},
            {"produto_id": item2}
        ]
    }
    response_post = client.post("/sugestoes/regras", json=payload)
    assert response_post.status_code == 201, f"Erro ao adicionar sugestão: {response_post.text}"


@when(parsers.cfparse('o sistema busca as sugestoes da "{mesa}"'), target_fixture="context")
def buscar_sugestoes(context, mesa):
    """
    Executa a chamada de API para obter as sugestões para a mesa configurada.
    """
    response = client.get(f"/sugestoes/{mesa}")
    context["response"] = response
    return context

@then(parsers.cfparse('o item "{produto_sugerido_id}" deve aparecer nas sugestoes'))
def verificar_item_sugerido(context, produto_sugerido_id):
    """
    Verifica se a resposta da API contém o item que deveria ser sugerido.
    """
    response = context["response"]
    assert response.status_code == 200, f"Status code inesperado: {response.status_code}. Response: {response.json()}"

    sugestoes = response.json()
    
    assert isinstance(sugestoes, list), "A resposta deveria ser uma lista."
    assert len(sugestoes) > 0, "A lista de sugestões não deveria estar vazia."

    # Verifica se o ID do produto sugerido está na lista de sugestões
    ids_sugeridos = [item["id"] for item in sugestoes]
    assert produto_sugerido_id in ids_sugeridos, \
        f"O item '{produto_sugerido_id}' não foi encontrado nas sugestões: {ids_sugeridos}"