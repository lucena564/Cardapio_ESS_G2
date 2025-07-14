import re
from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then, parsers
from src.main import app

client = TestClient(app)

@scenario(
    scenario_name="Adicionar dois itens ao pedido e verificar o total",
    feature_name="../features/fazer_um_pedido_com_dois_itens.feature"
)
def test_fazer_pedido_com_dois_itens():
    pass


@given(parsers.cfparse('estou na página do cardápio digital como cliente na "{mesa}"'), target_fixture="context")
def acessar_cardapio(mesa):
    return {
        "mesa": mesa,
        "itens": [],
        "total": 0
    }

@when(parsers.cfparse('adiciono o item "{produto_id}" com "{quantidade:d}" quantidade(s), totalizando "{valor_total}" reais ao carrinho'))
def adicionar_item(context, produto_id, quantidade, valor_total):
    """
        Preciso verificar se o item
    """
    item = {
        "produto_id": produto_id,
        "quantidade": quantidade
    }
    valor = valor_total
    context["itens"].append(item)
    context["total"] = context.get("total", 0) + (quantidade * float(valor))
    return context

@then("o pedido deve ser criado com sucesso")
def fazer_pedido_e_verificar(context):
    payload = {
        "mesa": context["mesa"],
        "itens": context["itens"]
    }
    response = client.post("/pedidos/", json=payload)
    
    print("\n\nResposta da API:", response.json())

    assert response.status_code == 201
    data = response.json()
    assert "message" in data and "sucesso" in data["message"].lower()
    assert "total" in data
    assert data["total"] > 0