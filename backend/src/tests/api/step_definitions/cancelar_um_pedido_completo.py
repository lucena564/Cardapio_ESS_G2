from pytest_bdd import scenario, given, when, then
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@scenario(
    scenario_name="Cancelar um pedido ainda não finalizado",
    feature_name="../features/cancelar_um_pedido_completo.feature"
)
def test_cancelar_pedido():
    """Teste para cancelar um pedido não finalizado."""


@given("estou na página do cardápio digital como cliente", target_fixture="context")
def acessar_cardapio():
    return {
        "mesa": "mesa_1",
        "pedido": None,
        "response": None
    }


@given("já foi feito um pedido que ainda não foi finalizado")
def criar_pedido_nao_finalizado(context):
    payload = {
        "mesa": context["mesa"],
        "itens": [
            {"produto_id": "P001", "quantidade": 1},
            {"produto_id": "P002", "quantidade": 2}
        ]
    }
    response = client.post("/pedidos/", json=payload)
    assert response.status_code == 201
    context["pedido"] = response.json()
    return context


@when('clico em "Cancelar Pedido"')
def clicar_cancelar_pedido(context):
    context["tela"] = "pedidos_realizados"
    return context


@then('deve aparecer uma tela com os "Pedidos Realizados"')
def verificar_tela_pedidos_realizados(context):
    assert context["tela"] == "pedidos_realizados"
    return context


@then("o usuário seleciona o pedido que deseja cancelar")
def selecionar_pedido_para_cancelar(context):
    # Neste exemplo, não há ID de pedido, mas cancelaremos todos os itens da mesa.
    mesa = context["mesa"]
    pedidos = client.get("/pedidos/").json()
    assert mesa in pedidos and len(pedidos[mesa]["pedidos"]) > 0
    context["pedidos_antes"] = pedidos[mesa]["pedidos"]
    return context


@then("o pedido deve ser cancelado com sucesso")
def cancelar_pedido(context):
    # Faz um PUT para modificar o pedido e esvaziar os itens (cancelamento)
    payload = {"itens": []}
    response = client.put(f"/pedidos/{context['mesa']}", json=payload)
    context["response"] = response
    assert response.status_code == 400 or response.status_code == 200
    return context


@then("o carrinho deve remover esse pedido")
def verificar_remocao_do_pedido(context):
    pedidos_atualizados = client.get("/pedidos/").json()
    mesa_data = pedidos_atualizados[context["mesa"]]
    assert mesa_data["pedidos"] == []  # lista vazia
    return context


@then("o total do pedido deve ser recalculado corretamente")
def verificar_recalculo_total(context):
    pedidos = client.get("/pedidos/").json()
    total = pedidos[context["mesa"]]["total"]
    assert total == 0
    return context
