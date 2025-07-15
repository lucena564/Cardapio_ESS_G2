Feature: Fechar Pedido de uma Mesa
  As a user of the system
  I want to close an active order for a table
  So that the order is moved to the history and the table becomes available

Background: O estado inicial do sistema
  Given o arquivo de pedidos ativos contém os seguintes dados para a "mesa_1", ids "B001" e "L001", quantidades "2" e "1" respectivamente e valor total "33" e o arquivo de histórico de pedidos está vazio para as outras mesas
  
  # Cenário de Sucesso
  Scenario: Fechar com sucesso um pedido ativo de uma mesa existente
    Given o arquivo de histórico de pedidos está inicialmente vazio
    When um cliente faz uma requisição POST para "/pedidos/fechar/mesa_1"
    Then o código de status da resposta deve ser 200
    And o corpo da resposta deve conter a mensagem "Pedido da mesa_1 fechado com sucesso e movido para o histórico."
    And o novo arquivo de histórico de pedidos deve conter 1 registro para a "mesa_1"
    And o novo registro no histórico deve ter o status "em andamento"
    And o arquivo de pedidos ativos para a "mesa_1" deve agora estar vazio

  # Cenários de Erro
  Scenario: Tentar fechar um pedido de uma mesa que não existe
    When um cliente faz uma requisição POST para "/pedidos/fechar/mesa_99"
    Then o código de status da resposta deve ser 404
    And o corpo da resposta deve conter a mensagem de erro "Mesa não encontrada."

  Scenario: Tentar fechar um pedido de uma mesa que não tem itens ativos
    When um cliente faz uma requisição POST para "/pedidos/fechar/mesa_2"
    Then o código de status da resposta deve ser 400
    And o corpo da resposta deve conter a mensagem de erro "Não há pedido ativo para fechar nesta mesa."

  # Cenário de Borda (Edge Case)
  Scenario: Fechar um pedido quando o histórico já contém outros pedidos
    Given o arquivo de histórico de pedidos já contém o seguinte registro de id_historico "0001" e mesa "mesa_1"
    When um cliente faz uma requisição POST para "/pedidos/fechar/mesa_1"
    Then o código de status da resposta deve ser 200
    And o novo arquivo de histórico de pedidos deve agora conter 2 registros
    And o novo registro no histórico deve ter o "id_historico" "0002"