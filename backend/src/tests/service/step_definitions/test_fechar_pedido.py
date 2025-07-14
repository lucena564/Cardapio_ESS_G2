# Em: tests/step_definitions/test_fechar_pedido_steps.py

import pytest
import json
import os
from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then, parsers

# Importe a instância principal da sua aplicação FastAPI
# O caminho pode precisar de ajuste dependendo da sua estrutura
from src.main import app 
import src.api.pedidos as pedidos_api

# Caminhos para os nossos arquivos de dados de teste
# É uma boa prática usar arquivos separados para os testes para não sujar os dados de desenvolvimento
PEDIDOS_ATIVOS_TEST_FILE = "test_pedidos_ativos.json"
HISTORICO_TEST_FILE = "test_historico.json"

# --- Cenários ---
# Esta linha diz ao pytest-bdd para procurar por cenários no arquivo .feature especificado
@scenario('../features/fechar_pedido.feature', 'Fechar com sucesso um pedido ativo de uma mesa existente')
def test_fechar_pedido_com_sucesso():
    pass

@scenario('../features/fechar_pedido.feature', 'Tentar fechar um pedido de uma mesa que não existe')
def test_fechar_pedido_mesa_inexistente():
    pass

@scenario('../features/fechar_pedido.feature', 'Tentar fechar um pedido de uma mesa que não tem itens ativos')
def test_fechar_pedido_mesa_sem_itens():
    pass

@scenario('../features/fechar_pedido.feature', 'Fechar um pedido quando o histórico já contém outros pedidos')
def test_fechar_pedido_com_historico_existente():
    pass


# --- Fixtures (Contexto e Ferramentas de Teste) ---
@pytest.fixture
def test_client(monkeypatch):
    """
    Cria um TestClient e usa monkeypatch para redirecionar as chamadas
    de leitura/escrita de arquivos para os arquivos de teste.
    """
    original_ler_pedidos = pedidos_api.ler_pedidos
    original_salvar_pedidos = pedidos_api.salvar_pedidos
    original_ler_historico = pedidos_api.ler_historico
    original_salvar_historico = pedidos_api.salvar_historico

    # --- PASSO 2: Definir os mocks para chamar as funções ORIGINAIS ---
    def mock_ler_pedidos(*args, **kwargs):
        # Agora chama a função original que guardamos
        return original_ler_pedidos(caminho_pedidos=PEDIDOS_ATIVOS_TEST_FILE)

    def mock_salvar_pedidos(data, *args, **kwargs):
        # Chama a função original que guardamos
        return original_salvar_pedidos(data, caminho_pedidos=PEDIDOS_ATIVOS_TEST_FILE)

    def mock_ler_historico(*args, **kwargs):
        return original_ler_historico(caminho_historico=HISTORICO_TEST_FILE)

    def mock_salvar_historico(data, *args, **kwargs):
        return original_salvar_historico(data, caminho_historico=HISTORICO_TEST_FILE)

    # Aplica o "patch": substitui a função no módulo da API pela nossa função mock
    monkeypatch.setattr(pedidos_api, "ler_pedidos", mock_ler_pedidos)
    monkeypatch.setattr(pedidos_api, "salvar_pedidos", mock_salvar_pedidos)
    monkeypatch.setattr(pedidos_api, "ler_historico", mock_ler_historico)
    monkeypatch.setattr(pedidos_api, "salvar_historico", mock_salvar_historico)

    # Retorna o cliente que agora usará as funções "enganadas"
    return TestClient(app)




'''@pytest.fixture
def test_client():
    """Cria uma instância do TestClient para fazer requisições à API."""
    return TestClient(app)
'''
@pytest.fixture
def context():
    """Um dicionário para passar dados entre os passos (ex: a resposta da API)."""
    return {}

@pytest.fixture(autouse=True)
def setup_teardown_files():
    """
    Esta fixture é executada automaticamente para cada teste.
    Ela limpa os arquivos de teste antes e depois de cada cenário.
    """
    # Setup: Garante que os arquivos de teste não existem no início
    if os.path.exists(PEDIDOS_ATIVOS_TEST_FILE):
        os.remove(PEDIDOS_ATIVOS_TEST_FILE)
    if os.path.exists(HISTORICO_TEST_FILE):
        os.remove(HISTORICO_TEST_FILE)
    
    yield 

    # Teardown: Limpa os arquivos novamente após o teste
    if os.path.exists(PEDIDOS_ATIVOS_TEST_FILE):
        os.remove(PEDIDOS_ATIVOS_TEST_FILE)
    if os.path.exists(HISTORICO_TEST_FILE):
        os.remove(HISTORICO_TEST_FILE)


# --- Step Definitions (Given, When, Then) ---

# BACKGROUND
@given('o arquivo de pedidos ativos contém os seguintes dados para a "mesa_1", ids "B001" e "L001", quantidades "2" e "1" respectivamente e valor total "33" e o arquivo de histórico de pedidos está vazio para as outras mesas')
def setup_default_active_orders():
    """Cria o arquivo de pedidos ativos com a estrutura base."""
    dados_base = {
        "mesas": ["mesa_1", "mesa_2", "mesa_3", "mesa_4", "mesa_5"],
        "mesa_1": {"pedidos": [{
                "produto_id": "B001",
                "quantidade": 2
            },
            {
                "produto_id": "L001",
                "quantidade": 1
            }],
            "total": 33.0},
        "mesa_2": {"pedidos": [], "total": 0},
        "mesa_3": {"pedidos": [], "total": 0},
        "mesa_4": {"pedidos": [], "total": 0},
        "mesa_5": {"pedidos": [], "total": 0},
    }
    with open(PEDIDOS_ATIVOS_TEST_FILE, "w") as f:
        json.dump(dados_base, f, indent=2)

'''
@given(parsers.parse('o arquivo de pedidos ativos para a "{mesa}" está vazio'), target_fixture="active_order_file_empty")
def mock_pedidos_ativos_vazio(mesa):
    dados = {
        "mesas": [mesa],
        mesa: {"pedidos": [], "total": 0}
    }
    with open(PEDIDOS_ATIVOS_TEST_FILE, "w") as f:
        json.dump(dados, f)
    return PEDIDOS_ATIVOS_TEST_FILE
'''
@given('o arquivo de histórico de pedidos está inicialmente vazio')
def mock_historico_vazio():
    # A fixture setup_teardown_files já garante isso
    pass

@given(parsers.parse('o arquivo de histórico de pedidos já contém o seguinte registro:'), target_fixture="history_file_with_data")
def mock_historico_com_dados():
    dados = [[
    {
        "id_historico": "0001",
        "mesa": "mesa_1",
        "itens": [
            {
                "produto_id": "B004",
                "nome": "Cerveja Heineken Long Neck",
                "quantidade": 3,
                "valor_unitario": 9.0,
                "categoria": "BEBIDAS"
            }
        ],
        "total": 46.3,
        "data_fechamento": "2025-07-13T11:47:52.506010",
        "status": "concluido"
    }]]
    with open(HISTORICO_TEST_FILE, "w") as f:
        json.dump(dados, f)
    return HISTORICO_TEST_FILE

'''@given(parsers.parse('o sistema não tem nenhuma informação sobre a "{mesa}"'))
def mock_mesa_inexistente(mesa):
    dados = {
        "mesas": ["mesa_1", "mesa_2"], # Uma lista de mesas que não inclui a mesa do teste
        "mesa_1": {},
        "mesa_2": {}
    }
    with open(PEDIDOS_ATIVOS_TEST_FILE, "w") as f:
        json.dump(dados, f)'''

@given(parsers.parse('o arquivo de histórico de pedidos já contém o seguinte registro de id_historico "0001" e mesa "mesa_1"'))
def mock_historico_com_registro_especifico():
    dados = [{
        "id_historico": "0001",
        "mesa": "mesa_1",
        "itens": [
            {
                "produto_id": "B004",
                "nome": "Cerveja Heineken Long Neck",
                "quantidade": 2,
                "valor_unitario": 9.0,
                "categoria": "BEBIDAS"
            }
        ],
        "total": 18.0,
        "data_fechamento": "2025-07-13T11:47:52.506010",
        "status": "concluido"
    }]
    with open(HISTORICO_TEST_FILE, "w") as f:
        json.dump(dados, f)


# Quando (When)
@when(parsers.parse('um cliente faz uma requisição POST para "{caminho}"'))
def fazer_requisicao_post(context, test_client, caminho):
    response = test_client.post(caminho)
    context["response"] = response

# Então (Then)
@then(parsers.parse('o código de status da resposta deve ser {codigo:d}'))
def verificar_status_code(context, codigo):
    assert context["response"].status_code == codigo

@then(parsers.parse('o corpo da resposta deve conter a mensagem "{mensagem}"'))
def verificar_mensagem_resposta(context, mensagem):
    response_data = context["response"].json()
    assert mensagem in response_data.get("message", "")

@then(parsers.parse('o corpo da resposta deve conter a mensagem de erro "{mensagem}"'))
def verificar_mensagem_erro_resposta(context, mensagem):
    response_data = context["response"].json()
    assert response_data.get("detail") == mensagem

@then(parsers.parse('o novo arquivo de histórico de pedidos deve conter {n:d} registro para a "{mesa}"'))
def verificar_registro_historico(n, mesa):
    with open(HISTORICO_TEST_FILE, "r") as f:
        historico = json.load(f)
    registros_da_mesa = [p for p in historico if p['mesa'] == mesa]
    assert len(registros_da_mesa) == n

@then(parsers.parse('o arquivo de pedidos ativos para a "{mesa}" deve agora estar vazio'))
def verificar_pedidos_ativos_zerado(mesa):
    with open(PEDIDOS_ATIVOS_TEST_FILE, "r") as f:
        pedidos_ativos = json.load(f)
    assert not pedidos_ativos[mesa]["pedidos"] # Verifica se a lista de pedidos está vazia
    assert pedidos_ativos[mesa]["total"] == 0

@then(parsers.parse('o novo arquivo de histórico de pedidos deve agora conter {n:d} registros'))
def verificar_total_registros_historico(n):
    with open(HISTORICO_TEST_FILE, "r") as f:
        historico = json.load(f)
    assert len(historico) == n

@then(parsers.parse('o novo registro no histórico deve ter o "id_historico" "{id_}"'))
def verificar_id_incremental(id_):
    with open(HISTORICO_TEST_FILE, "r") as f:
        historico = json.load(f)
    # O novo registro é o último adicionado
    assert historico[-1]["id_historico"] == id_

@then(parsers.parse('o novo registro no histórico deve ter o status "{status}"'))
def verificar_status(status):
    with open(HISTORICO_TEST_FILE, "r") as f:
        historico = json.load(f)
    # O novo registro é o último adicionado
    assert historico[-1]["status"] == status