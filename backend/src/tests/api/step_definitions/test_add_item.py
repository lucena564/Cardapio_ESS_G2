
from pytest_bdd import scenario, given, when, then, parsers
from fastapi.testclient import TestClient
from src.main import app

# Cria o cliente de teste como uma variável no escopo do módulo
client = TestClient(app)

# Definição do Cenário
@scenario(
    feature_name="../features/add_item.feature",
    scenario_name="Administrador adiciona um novo item ao cardápio"
)
def test_add_new_item():
    """Define o teste para o cenário de adição de item."""
    pass

# Implementação dos Passos

@given("que o administrador está no cardapio", target_fixture="context")
def admin_on_menu(context):
    """Prepara o contexto inicial para o teste."""
    return {}

@when(parsers.parse('ele decide cadastrar "{nome}", com a descrição "{descricao}", preço "{preco}" e categoria "{categoria}"'), target_fixture="context")
def prepare_and_send_item_data(context, nome, descricao, preco, categoria):
    """Prepara o payload e envia a requisição POST para criar o item."""
    payload = {
        "NOME": nome,
        "DESCRICAO": descricao,
        "PRECO": float(preco),
        "CATEGORIA": categoria,
        "DESCONTO": 0
    }
    
    response = client.post("/admin/items/", json=payload)
    context["response"] = response
    return context

@then(parsers.parse('o novo item "{nome_item}" deve ser criado com sucesso no sistema'))
def check_creation_success(context, nome_item):
    """Verifica se a API respondeu corretamente, indicando que o item foi criado."""
    response = context["response"]
    assert response.status_code == 201

    response_data = response.json()
    assert response_data["NOME"] == nome_item
    assert "ID" in response_data
    assert response_data["ID"] is not None

    context["new_item_id"] = response_data["ID"]

@then(parsers.parse('o item "{nome_item}" deve estar disponível para consulta no cardápio'))
def verify_item_in_list(context, nome_item):
    """
    Verifica se o item recém-criado realmente existe no sistema,
    fazendo uma nova requisição para listar todos os itens.
    """
    response = client.get("/admin/items/")
    assert response.status_code == 200
    
    items_list = response.json()
    found_item = next((item for item in items_list if item["ID"] == context["new_item_id"]), None)
    
    assert found_item is not None
    assert found_item["NOME"] == nome_item