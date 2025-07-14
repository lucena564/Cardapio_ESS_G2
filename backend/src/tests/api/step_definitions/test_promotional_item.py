
from pytest_bdd import scenario, given, when, then, parsers
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@scenario(
    feature_name="../features/promotional_item.feature",
    scenario_name="Administrador define um item como promocional"
)
def test_add_promotion_to_item():
    pass


@given(parsers.parse('que o item "{nome_item}" existe com o preço de "{preco}" e sem desconto'), target_fixture="context")
def existing_item_without_promotion(context, nome_item, preco):
    """Garante que um item sem desconto exista no sistema, criando-o via API."""
    payload = {"NOME": nome_item, "DESCRICAO": "Item para teste", "PRECO": float(preco), "DESCONTO": 0, "CATEGORIA": "OUTROS"}
    response = client.post("/admin/items/", json=payload)
    assert response.status_code == 201
    context["item_id"] = response.json()["ID"]
    return context


@when(parsers.parse('o administrador decide aplicar um desconto de "{desconto}" por cento para o item "{nome_item}"'), target_fixture="context")
def apply_discount(context, desconto, nome_item):
    """Envia a requisição PUT para adicionar o desconto."""
    update_payload = {"DESCONTO": int(desconto)}

    item_id = context["item_id"]
    response = client.put(f"/admin/items/{item_id}", json=update_payload)

    context["response"] = response
    return context


@then("a promoção deve ser aplicada com sucesso")
def check_promotion_update_success(context):
    """Verifica se a API retornou sucesso (200 OK)."""
    assert context["response"].status_code == 200


@then(parsers.parse('o item "{nome_item}" deve agora ter um desconto de "{desconto}" por cento'))
def check_updated_discount(context, nome_item, desconto):
    """Verifica se o corpo da resposta reflete o desconto atualizado."""
    response_data = context["response"].json()
    assert response_data["NOME"] == nome_item
    assert response_data["DESCONTO"] == int(desconto)