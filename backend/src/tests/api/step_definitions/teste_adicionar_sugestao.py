import json
import os
from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then, parsers
from src.main import app
from Utils.constants import Constants

client = TestClient(app)

# Caminho para o arquivo de regras de sugestão
SUGESTOES_FILE_PATH = Constants.SUGESTOES_FILE


@scenario(
    "../features/adicionar_sugestao.feature",
    "Adicionando uma sugestao de combinacoes"
)
def test_adicionar_sugestao():
    pass

@given("estou logado como admin", target_fixture="context")
def context_inicial():
    """Inicializa o contexto do teste."""
    return {}

@given('a sugestao "MistoQuenteComSuco" nao esta cadastrada no sistema')
def garantir_estado_sem_sugestao():
    response = client.get("/sugestoes/regras")
    assert response.status_code == 200
    regras_atuais = response.json()

    for regra in regras_atuais:
        if regra["nome"] == "MistoQuenteComSuco":
            delete_response = client.delete(f"/sugestoes/regras/MistoQuenteComSuco")
            assert delete_response.status_code == 200
            break

@when(parsers.cfparse('eu seleciono para adicionar a sugestao "{nome_sugestao}" com items "{item1}" e "{item2}"'), target_fixture="context")
def adicionar_nova_sugestao(context, nome_sugestao, item1, item2):
    """
    Simula a chamada de API para adicionar uma nova regra de sugestão,
    enviando o payload no formato esperado pela API.
    """
    payload = {
        "nome": nome_sugestao,
        "combinacao": [
            {"produto_id": item1},
            {"produto_id": item2}
        ]
    }
    response = client.post("/sugestoes/regras", json=payload)
    context["response"] = response
    return context

@then("a sugestao foi adicionada com sucesso")
def verificar_resposta_sucesso_adicao(context):
    """
    Verifica se a API respondeu corretamente, com status 201 CREATED
    e uma mensagem de sucesso.
    """
    response = context["response"]
    assert response.status_code == 201, f"Status code inesperado: {response.status_code}. Response: {response.json()}"
    
    response_data = response.json()
    assert "message" in response_data
    assert "adicionada com sucesso" in response_data["message"]
    assert response_data["nome_regra_adicionada"] == "MistoQuenteComSuco"

@then(parsers.cfparse('a sugestao "{nome_sugestao}" deve aparecer no sistema'))
def verificar_se_sugestao_existe(nome_sugestao):
    """
    Verifica se a nova regra de sugestão foi de fato persistida,
    consultando a lista completa de regras via API.
    """
    response = client.get("/sugestoes/regras")
    assert response.status_code == 200
    
    regras_atuais = response.json()
    # Procura pela regra com o nome especificado na lista retornada
    sugestao_encontrada = any(regra["nome"] == nome_sugestao for regra in regras_atuais)
    
    assert sugestao_encontrada, f"A sugestão '{nome_sugestao}' não foi encontrada na API após a adição."