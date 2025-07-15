import json
import os
from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then, parsers
from src.main import app  # Importe a sua instância principal do FastAPI
from Utils.constants import Constants # Importe suas constantes para o caminho do arquivo

# Cria um cliente de teste para a sua aplicação FastAPI
client = TestClient(app)

# Caminho para o arquivo de regras de sugestão usado nos testes
SUGESTOES_FILE_PATH = Constants.SUGESTOES_FILE



# --- Cenário de Teste ---

@scenario(
    "../features/remover_sugestao.feature",
    "Excluindo uma sugestao das combinacoes"
)
def test_excluir_sugestao():
    """Define o cenário de teste BDD a ser executado."""
    pass



@given("estou logado como admin", target_fixture="context")
def context_inicial():
    """
    Inicializa o contexto do teste. No futuro, isso poderia conter
    tokens de autenticação, etc. Por enquanto, apenas retorna um dicionário vazio.
    """
    return {}

@given(parsers.cfparse('a sugestao "{nome_sugestao}" esteja cadastrada no sistema com items "{item1}" e "{item2}"'))
def garantir_estado_inicial_sugestoes(nome_sugestao, item1, item2):
    """
    Garante que a sugestão especificada esteja presente no sistema,
    criando-a via API caso ainda não exista.
    """
    # Verifica se a sugestão já existe
    response = client.get("/sugestoes/regras")
    assert response.status_code == 200
    regras_atuais = response.json()

    for regra in regras_atuais:
        if regra["nome"] == nome_sugestao:
            return  # Já existe, nada a fazer

    # Se não existe, cria usando a API
    payload = {
        "nome": nome_sugestao,
        "combinacao": [
            {"produto_id": item1},
            {"produto_id": item2}
        ]
    }

    response_post = client.post("/sugestoes/regras", json=payload)
    assert response_post.status_code == 201, f"Erro ao criar sugestão: {response_post.text}"



@when(parsers.cfparse('eu seleciono para excluir a sugestao "{nome_sugestao}"'), target_fixture="context")
def excluir_sugestao(context, nome_sugestao):
    """
    Simula a chamada de API para deletar a regra de sugestão especificada.
    """
    # Faz a requisição DELETE para o endpoint correspondente
    response = client.delete(f"/sugestoes/regras/{nome_sugestao}")
    
    # Armazena a resposta no contexto para validações futuras no 'then'
    context["response"] = response
    return context

@then("a sugestao foi excluida com sucesso")
def verificar_resposta_sucesso(context):
    """
    Verifica se a API respondeu com sucesso à requisição de exclusão.
    """
    response = context["response"]
    
    # Valida o código de status HTTP (200 OK para sucesso no delete)
    assert response.status_code == 200
    
    # Valida o conteúdo da mensagem de resposta
    response_data = response.json()
    assert "message" in response_data
    assert "deletada com sucesso" in response_data["message"]


@then(parsers.cfparse('a sugestao "{nome_sugestao}" nao deve mais existir no sistema'))
def verificar_exclusao_da_sugestao(nome_sugestao):
    """
    Verifica se a regra de sugestão foi de fato removida, tanto no arquivo
    quanto ao consultar a lista de regras via API.
    """
    # 1. Verificação via API (método preferencial)
    response_get = client.get("/sugestoes/regras")
    assert response_get.status_code == 200
    
    regras_atuais = response_get.json()
    # Verifica se a sugestão com o nome deletado não está na lista retornada
    sugestao_encontrada = any(regra["nome"] == nome_sugestao for regra in regras_atuais)
    assert not sugestao_encontrada, f"A sugestão '{nome_sugestao}' ainda foi encontrada na API após a exclusão."

    # 2. Verificação direta no arquivo (garantia adicional)
    with open(SUGESTOES_FILE_PATH, "r", encoding="utf-8") as f:
        dados_arquivo = json.load(f)
    
    assert nome_sugestao not in dados_arquivo["nomes_sugestao"]
    assert nome_sugestao not in dados_arquivo