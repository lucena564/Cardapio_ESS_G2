from pytest_bdd import scenario, given, when, then


@scenario(
    scenario_name="Tentar cancelar pedido sem nenhum pedido realizado",
    feature_name="../features/cancelar_um_pedido_com_a_mesa_zerada.feature"
)
def test_cancelar_sem_pedido():
    """Teste para tentar cancelar um pedido que não existe."""


@given("estou na página do cardápio digital como cliente", target_fixture="context")
def acessar_cardapio():
    return {
        "pedidos": [],
        "tela": "cardapio",
        "mensagem": None
    }


@given("não realizei um pedido", target_fixture="context")
def sem_pedido(context):
    assert len(context["pedidos"]) == 0
    return context


@when('clico em "Cancelar Pedido"', target_fixture="context")
def clicar_cancelar(context):
    if not context["pedidos"]:
        context["mensagem"] = "Não existe um pedido da mesa ainda"
    else:
        context["tela"] = "pedidos_realizados"
    return context


@then("deve ser mostrado uma mensagem ao usuário que não existe um pedido da mesa ainda", target_fixture="context")
def verificar_mensagem_erro(context):
    assert context["mensagem"] == "Não existe um pedido da mesa ainda"
    return context
