from pytest_bdd import scenario, given, when, then, parsers
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@scenario(
    scenario_name="Editar um pedido removendo um item",
    feature_name="../features/cancelar_um_item_especifico_do_pedido.feature"
)
def test_editar_pedido():
    pass


@given("estou na página do cardápio digital como cliente", target_fixture="context")
def acessar_cardapio():
    return {
        "mesa": "mesa_3",
        "pedido": None,
        "response": None
    }


@given('adiciono os itens "Suco de Laranja" de "10" reais e "X-Burger" de "20" reais')
def adicionar_itens(context):
    payload = {
        "mesa": context["mesa"],
        "itens": [
            {"produto_id": "P001", "quantidade": 1}, # Peguei id do dados.json / Não necessáriamente o do Suco de Laranja, apenas pra teste.
            {"produto_id": "P002", "quantidade": 1}  # Peguei id do dados.json / Não necessáriamente o do X-Burger, apenas pra teste.
        ]
    }
    response = client.post("/pedidos/", json=payload)
    assert response.status_code == 201
    context["pedido_original"] = response.json()
    return context


@given('clico em "Fazer Pedido"')
def confirmar_pedido(context):
    assert context["pedido_original"]["message"].lower().startswith("pedido realizado")
    return context


@when('clico em "Editar Pedido"')
def clicar_editar(context):
    context["tela"] = "editar"
    return context


@then("janela com os pedidos realizados é aberta")
def abrir_pedidos(context):
    assert context["tela"] == "editar"
    return context


@then("seleciono o pedido que acabou de ser computado")
def selecionar_pedido(context):
    assert context.get("pedido_original") is not None
    return context


@then('removo o item "Suco de Laranja"')
def remover_item(context):
    # Reenvia pedido com apenas "X-Burger"
    payload = {
        "itens": [
            {"produto_id": "P002", "quantidade": 1}
        ]
    }
    response = client.put(f"/pedidos/{context['mesa']}", json=payload)
    assert response.status_code == 200
    context["pedido_modificado"] = response.json()
    return context


@then('clico em "Atualizar Pedido"')
def atualizar_pedido(context):
    assert context["pedido_modificado"]["message"].lower().startswith("pedido modificado")
    return context


@then('o pedido deve conter apenas o item "X-Burger"')
def verificar_item_restante(context):
    pedidos = client.get("/pedidos/").json()
    itens = pedidos[context["mesa"]]["pedidos"]
    assert len(itens) == 1
    assert itens[0]["produto_id"] == "P002"
    return context


@then("o total do pedido deve ser recalculado")
def verificar_total(context):
    pedidos = client.get("/pedidos/").json()
    total = pedidos[context["mesa"]]["total"]
    assert total == 50.0  # P002 50.0 no dados.json
    return context
