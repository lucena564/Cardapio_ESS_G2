import pytest
import json
import os
from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then, parsers
from src.main import app
import src.api.order_history as historico_api 

# Constante para o arquivo de teste
HISTORICO_TEST_FILE = "test_historico.json"

# --- Cenários ---
@scenario('../features/historico.feature', 'Consultar com sucesso o histórico de uma mesa com pedidos existentes')
def test_cenario_consultar_historico():
    pass

@scenario('../features/historico.feature', 'Tentar consultar o histórico de uma mesa que não possui registros')
def test_cenario_consultar_mesa_vazia():
    pass

@scenario('../features/historico.feature', 'Atualizar com sucesso o status de um pedido existente')
def test_cenario_atualizar_pedido():
    pass

@scenario('../features/historico.feature', 'Tentar atualizar um pedido com um ID que não existe')
def test_cenario_atualizar_id_invalido():
    pass

@scenario('../features/historico.feature', 'Deletar múltiplos pedidos do histórico com sucesso')
def test_cenario_deletar_pedidos():
    pass

@scenario('../features/historico.feature', 'Filtrar o histórico de uma mesa por status com sucesso')
def test_cenario_filtrar_por_status():
    pass

@scenario('../features/historico.feature', 'Filtrar o histórico de uma mesa por categoria e data combinados')
def test_cenario_filtrar_combinado():
    pass

@scenario('../features/historico.feature', 'Realizar uma busca com filtros que não retorna nenhum resultado')
def test_cenario_filtrar_sem_resultado():
    pass

# --- Fixtures ---

@pytest.fixture
def test_client(monkeypatch):
    """Prepara o cliente de teste com monkeypatching para isolar os arquivos."""
    original_ler = historico_api.ler_historico
    original_salvar = historico_api.salvar_historico

    def mock_ler(*args, **kwargs):
        return original_ler(caminho=HISTORICO_TEST_FILE)
    
    def mock_salvar(data, *args, **kwargs):
        return original_salvar(data, caminho=HISTORICO_TEST_FILE)

    monkeypatch.setattr(historico_api, "ler_historico", mock_ler)
    monkeypatch.setattr(historico_api, "salvar_historico", mock_salvar)
    
    return TestClient(app)

@pytest.fixture
def context():
    """Dicionário para passar a resposta da API entre os passos."""
    return {}

@pytest.fixture
def historico_state():
    """
    Uma fixture mais robusta para gerenciar o estado do histórico.
    É uma lista que acumulamos nos passos 'Given'.
    """
    return []

@pytest.fixture(autouse=True)
def setup_teardown_files(historico_state):
    """Limpa o arquivo de teste e reseta o estado antes e depois de cada cenário."""
    if os.path.exists(HISTORICO_TEST_FILE):
        os.remove(HISTORICO_TEST_FILE)
    
    # Reseta a lista de estado
    historico_state.clear()

    yield

    if os.path.exists(HISTORICO_TEST_FILE):
        os.remove(HISTORICO_TEST_FILE)

def salvar_estado_no_arquivo(state):
    """Função auxiliar para salvar o estado atual no arquivo de teste."""
    with open(HISTORICO_TEST_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

# --- Step Definitions ---

# GIVEN
@given('o arquivo de histórico está vazio')
def historico_vazio():
    salvar_estado_no_arquivo([])

@given(parsers.parse('que existe no histórico um pedido com id_historico "{id_}", mesa "{mesa}", total {total:f}, data_fechamento "{data}" e status "{status}"'))
def setup_pedido_base(historico_state, id_, mesa, total, data, status):
    novo_pedido = {
        "id_historico": id_,
        "mesa": mesa,
        "itens": [], # Começa com itens vazios
        "total": total,
        "data_fechamento": data,
        "status": status
    }
    historico_state.append(novo_pedido)
    salvar_estado_no_arquivo(historico_state)

@given(parsers.parse('o pedido "{id_pedido}" possui um item com produto_id "{prod_id}", nome "{nome}", quantidade {qtd:d}, valor_unitario {valor:f} e categoria "{cat}"'))
def adicionar_item_ao_pedido(historico_state, id_pedido, prod_id, nome, qtd, valor, cat):
    # Encontra o pedido na nossa lista de estado
    pedido_alvo = next((p for p in historico_state if p["id_historico"] == id_pedido), None)
    if pedido_alvo:
        novo_item = {
            "produto_id": prod_id,
            "nome": nome,
            "quantidade": qtd,
            "valor_unitario": valor,
            "categoria": cat
        }
        pedido_alvo["itens"].append(novo_item)
    salvar_estado_no_arquivo(historico_state)

# WHEN
@when(parsers.parse('um cliente faz uma requisição GET para "{caminho}"'))
def fazer_requisicao_get(context, test_client, caminho):
    context["response"] = test_client.get(caminho)

@when(parsers.parse('um cliente faz uma requisição PUT para "/historico/{id_historico}" com o seguinte corpo: id_historico "{id_}", mesa "{mesa}", total {total:f}, data_fechamento "{data}" e status "{status}" e possui um item com produto_id "P001", nome "Pizza Margherita", quantidade 1, valor_unitario 45.0 e categoria "PIZZAS"'))
def fazer_requisicao_put_literal(context, test_client, id_historico, id_, mesa, total, data, status):
    # Para o PUT, precisamos construir o payload completo, incluindo os itens.
    # Vamos assumir que os itens são os mesmos do estado inicial para este cenário.
    pedido_existente = historico_api.ler_historico()[0] # Simplificação para o cenário
    payload = {
        "id_historico": id_,
        "mesa": mesa,
        "itens": pedido_existente['itens'], # Reutiliza os itens
        "total": total,
        "data_fechamento": data,
        "status": status
    }
    context["response"] = test_client.put(f"/historico/{id_historico}", json=payload)

@when('um cliente faz uma requisição PUT para "/historico/9999" com um corpo JSON válido')
def fazer_requisicao_put_invalido(context, test_client):
    payload_valido = {
        "id_historico": "9999", "mesa": "mesa_9", "itens": [], "total": 0,
        "data_fechamento": "2025-01-01T00:00:00", "status": "concluido"
    }
    context["response"] = test_client.put("/historico/9999", json=payload_valido)
    
@when(parsers.parse('um cliente faz uma requisição DELETE para "{caminho}" com o seguinte corpo "{ids_historico}"'))
def fazer_requisicao_delete(context, test_client, caminho, ids_historico):
    payload = {
        "ids_historico": [id.strip() for id in ids_historico.split("e")]
    }
    payload_str = json.dumps(payload)  
    response = test_client.request("DELETE",
    caminho,
    content=payload_str,
    headers={"Content-Type": "application/json"}
    )

    context["response"] = response


# THEN 
@then(parsers.parse('o código de status da resposta deve ser {codigo:d}'))
def verificar_status_code(context, codigo):
    assert context["response"].status_code == codigo

@then(parsers.parse('o corpo da resposta deve ser uma lista JSON contendo {n:d} pedidos'))
def verificar_tamanho_lista_resposta(context, n):
    response_data = context["response"].json()
    assert isinstance(response_data, list)
    assert len(response_data) == n

@then(parsers.parse('a resposta deve conter um pedido com "id_historico" igual a "{id_}"'))
def verificar_presenca_pedido(context, id_):
    response_data = context["response"].json()
    assert any(p.get("id_historico") == id_ for p in response_data)

@then(parsers.parse('a resposta não deve conter um pedido com "id_historico" igual a "{id_}"'))
def verificar_ausencia_pedido(context, id_):
    response_data = context["response"].json()
    assert not any(p.get("id_historico") == id_ for p in response_data)

@then(parsers.parse('o corpo da resposta deve conter a mensagem de erro "{mensagem}"'))
def verificar_mensagem_erro(context, mensagem):
    assert context["response"].json()["detail"] == mensagem

@then(parsers.parse('o pedido com "id_historico" "{id_}" no arquivo de histórico deve agora ter o status "{status}"'))
def verificar_status_no_arquivo(id_, status):
    historico = historico_api.ler_historico(caminho=HISTORICO_TEST_FILE)
    pedido_alvo = next((p for p in historico if p["id_historico"] == id_), None)
    assert pedido_alvo is not None
    assert pedido_alvo["status"] == status

@then(parsers.parse('o corpo da resposta deve conter a mensagem "{mensagem}"'))
def verificar_mensagem_sucesso(context, mensagem):
    assert mensagem in context["response"].json()["message"]
    
@then(parsers.parse('o arquivo de histórico deve agora conter apenas {n:d} pedido'))
def verificar_tamanho_arquivo(n):
    historico = historico_api.ler_historico(caminho=HISTORICO_TEST_FILE)
    assert len(historico) == n

@then(parsers.parse('o arquivo de histórico não deve mais conter um pedido com "id_historico" "{id_}"'))
def verificar_ausencia_no_arquivo(id_):
    historico = historico_api.ler_historico(caminho=HISTORICO_TEST_FILE)
    assert not any(p["id_historico"] == id_ for p in historico)

@then(parsers.parse('todos os pedidos na resposta devem ter o status "{status}"'))
def verificar_status_na_resposta(context, status):
    response_data = context["response"].json()
    assert all(p["status"] == status for p in response_data)

@then('o corpo da resposta deve ser uma lista JSON vazia "[]"')
def verificar_resposta_vazia(context):
    assert context["response"].json() == []

@then(parsers.parse('o pedido na resposta deve ter o "id_historico" "{id_}"'))
def verificar_id_resposta(context, id_):
    assert context["response"].json()[0]["id_historico"] == id_