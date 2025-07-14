
from pytest_bdd import scenario, given, when, then, parsers
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@scenario(
    feature_name="../features/update_item.feature",
    scenario_name="Administrador atualiza o preço de um item existente"
)
def test_update_item():
    pass


@given(parsers.parse('que o item "{nome_item}" já existe no sistema com o preço de "{preco}"'), target_fixture="context")
def existing_item(client: TestClient, context, nome_item, preco):
    """Garante que um item exista no DB para ser usado no teste, criando-o via API."""
    # Limpa a base de dados para garantir um estado limpo (opcional, mas recomendado)
    # salvar_db({"produtos": [], "categorias": [...]}) 

    payload = {"NOME": nome_item, "DESCRICAO": "Item de teste para atualização", "PRECO": float(preco), "CATEGORIA": "PIZZAS"}
    response = client.post("/admin/items/", json=payload)
    assert response.status_code == 201

    context["item_id"] = response.json()["ID"]
    return context


@when(parsers.parse('o administrador decide atualizar o preço do item "{nome_item}" para "{novo_preco}"'), target_fixture="context")
def update_the_item(client: TestClient, context, nome_item, novo_preco):
    """Prepara o payload de atualização e envia a requisição PUT."""
    update_payload = {"PRECO": float(novo_preco)}

    item_id = context["item_id"]
    response = client.put(f"/admin/items/{item_id}", json=update_payload)

    context["response"] = response
    return context


@then("a atualização deve ser bem-sucedida")
def check_update_success(context):
    """Verifica se o status code da resposta é 200 (OK)."""
    assert context["response"].status_code == 200


@then(parsers.parse('o item "{nome_item}" deve agora custar "{novo_preco}"'))
def check_updated_price(context, nome_item, novo_preco):
    """Verifica se o corpo da resposta reflete o preço atualizado."""
    response_data = context["response"].json()
    assert response_data["NOME"] == nome_item
    assert response_data["PRECO"] == float(novo_preco)