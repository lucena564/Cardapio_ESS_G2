from pytest_bdd import scenario, given, when, then, parsers
from fastapi.testclient import TestClient
from src.main import app
import pytest

client = TestClient(app)

# Fixture para compartilhar dados entre steps
@pytest.fixture
def context():
    return {}

# Cada cenário da feature é relacionado a uma função de teste

@scenario("../features/categories.feature", "Adicionar uma nova categoria")
def test_adicionar_categoria():
    pass

@scenario("../features/categories.feature", "Impedir criação de categoria com nome duplicado")
def test_categoria_duplicada():
    pass

@scenario("../features/categories.feature", "Impedir criação de nova categoria sem informar um nome")
def test_categoria_nome_vazio():
    pass

@scenario("../features/categories.feature", "Excluir uma categoria existente")
def test_excluir_categoria():
    pass

@scenario("../features/categories.feature", "Impedir exclusão de categoria inexistente")
def test_excluir_categoria_inexistente():
    pass

@scenario("../features/categories.feature", "Atualizar o nome de uma categoria existente")
def test_atualizar_categoria():
    pass

@scenario("../features/categories.feature", "Impedir atualização de categoria inexistente")
def test_atualizar_categoria_inexistente():
    pass

# Steps Given para garantir o estado inicial da lista de categorias

@given(parsers.parse('não há categoria com nome "{nome}"'))
def garantir_categoria_nao_existe(nome):
    """ 
    Remove a categoria se ela existir,
    caso outro teste tenha criado essa categoria antes
    """
    resp = client.get("/categorias/")
    categorias = resp.json()
    if nome in categorias:
        client.delete(f"/categorias/{nome}")

@given(parsers.parse('já existe uma categoria chamada "{nome}"'))
def garantir_categoria_existe(nome):
    """ 
    Cria a categoria se ela não existir,
    caso outro teste tenha removido esta categoria
    """
    resp = client.get("/categorias/")
    categorias = resp.json()
    if nome not in categorias:
        client.post("/categorias/", json={"categoria": nome})

# Steps When para criação, atualização e exclusão de categorias

@when(parsers.parse('crio uma nova categoria com nome "{nome}"'))
def criar_categoria(context, nome):
    # Cria uma nova categoria e armazena a resposta
    context["response"] = client.post("/categorias/", json={"categoria": nome})

@when('crio uma nova categoria sem informar um nome')
def criar_categoria_nome_vazio(context):
    context["response"] = client.post("/categorias/", json={"categoria": ""})

@when(parsers.parse('excluo a categoria "{nome}"'))
def excluir_categoria(context, nome):
    # Exclui uma categoria existente.
    context["response"] = client.delete(f"/categorias/{nome}")

@when(parsers.parse('atualizo o nome da categoria de "{nome_antigo}" para "{nome_novo}"'))
def atualizar_categoria(context, nome_antigo, nome_novo):
    # Atualiza o nome de uma categoria.
    context["response"] = client.put(f"/categorias/{nome_antigo}", json={"categoria": nome_novo})

# Steps Then para verificação de resultados das operações 

@then(parsers.parse('a categoria "{nome}" deve estar presente na lista'))
def categoria_presente(nome):
    # Verifica se a categoria está na lista
    resp = client.get("/categorias/")
    categorias = resp.json()
    assert nome in categorias

@then(parsers.parse('a categoria "{nome}" não deve estar presente na lista'))
def categoria_ausente(nome):
    # Verifica se a categoria não está na lista
    resp = client.get("/categorias/")
    categorias = resp.json()
    assert nome not in categorias

@then("a categoria '' não deve estar presente na lista")
def categoria_vazia_ausente():
    # Caso em que impede a categoria vazia de ser criada e não listada
    resp = client.get("/categorias/")
    categorias = resp.json()
    assert "" not in categorias

@then('o sistema deve exibir uma mensagem de erro indicando que a categoria já existe')
def erro_categoria_ja_existe(context):
    # Verifica se a resposta foi erro 400
    assert context["response"].status_code == 400
    assert "já existe" in context["response"].json()["detail"].lower()

@then('o sistema deve exibir uma mensagem de erro indicando que o nome é obrigatório')
def erro_nome_obrigatorio(context):
    # Verifica se a resposta foi erro 400
    assert context["response"].status_code == 400
    assert "obrigatório" in context["response"].json()["detail"].lower()

@then('o sistema deve exibir uma mensagem de sucesso indicando que a categoria foi excluída')
def sucesso_exclusao(context):
    # Verifica se a resposta foi sucesso com código 200
    assert context["response"].status_code == 200
    assert "removida" in context["response"].json()["mensagem"].lower()

@then('o sistema deve exibir uma mensagem de erro indicando que a categoria não foi encontrada')
def erro_categoria_nao_encontrada(context):
    # Verifica se a resposta foi erro 404
    assert context["response"].status_code == 404
    assert "não encontrada" in context["response"].json()["detail"].lower()