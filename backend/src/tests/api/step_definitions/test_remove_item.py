# Arquivo: tests/step_definitions/test_remove_item.py

from pytest_bdd import scenario, given, when, then, parsers
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@scenario(
    feature_name="../features/remove_item.feature",
    scenario_name="Administrador remove um item existente"
)
def test_remove_item():
    pass

@given('que o item "Suco de Laranja" já existe no sistema', target_fixture="context")
def existing_item_to_remove(context):
    """
    Garante que um item exista para ser removido.
    Para isolar o teste, criamos um item novo a cada execução.
    """
    payload = {"NOME": "Suco de Laranja", "DESCRICAO": "Laranja pura", "PRECO": 7.00, "CATEGORIA": "BEBIDAS"}
    response = client.post("/admin/items/", json=payload)
    assert response.status_code == 201

    # Guarda o ID do item criado para usar nos próximos passos
    context["item_id"] = response.json()["ID"]
    return context


@when('o administrador decide remover o item "Suco de Laranja"', target_fixture="context")
def remove_the_item(context):
    """Envia a requisição DELETE para a API."""
    item_id = context["item_id"]
    response = client.delete(f"/admin/items/{item_id}")
    context["response"] = response
    return context


@then("a remoção deve ser bem-sucedida")
def check_removal_success(context):
    """Verifica se o status code da resposta é 204 (No Content)."""
    assert context["response"].status_code == 204


# Esta é a linha que foi corrigida para corresponder EXATAMENTE ao .feature
@then(parsers.parse('o item "{nome_item}" não deve mais ser encontrado no cardápio'))
def verify_item_is_gone(nome_item, context):
    """
    Verifica se o item foi realmente removido,
    listando todos os itens e garantindo que o ID removido não está na lista.
    """
    item_id_removido = context["item_id"]

    response = client.get("/admin/items/")
    assert response.status_code == 200

    lista_de_itens = response.json()

    # Verifica se algum item na lista atual tem o mesmo ID do que foi removido
    item_encontrado = any(item['ID'] == item_id_removido for item in lista_de_itens)

    # O teste passa se o item NÃO for encontrado
    assert not item_encontrado, f"O item '{nome_item}' com ID {item_id_removido} ainda foi encontrado."