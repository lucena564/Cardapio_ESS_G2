Feature: Gerenciamento do Histórico de Pedidos
  As a user of the system
  I want to be able to view, update, delete and filter historical orders
  To ensure data is accessible and can be managed correctly.





# ----------------------------------------------------------------
# Cenários para: Ler Histórico
# ----------------------------------------------------------------
  Scenario: Tentar ler um histórico vazio
    Given o historico tem 0 pedidos
    When ler_historico é chamado para "data/order_history.json"
    Then o deve ser retornado uma lista vazia

  Scenario: Tentar ler um caminho para o historico que não existe
    Given o caminho "data/order_history.json" não existe no sistema
    When ler_historico é chamado para "data/order_history.json"
    Then o deve ser retornado uma lista vazia

  Scenario: Ler um historico com 1 pedido
    Given o caminho "data/order_history.json" é um json com 1 pedido
    And o json tem o pedido com id_historico "0001", mesa "mesa_1", total 46.3, data_fechamento "2025-07-13T11:47:52.506010" e status "concluido"
    And o pedido "0001" possui um item com produto_id "B004", nome "Cerveja Heineken Long Neck", quantidade 3, valor_unitario 9.0 e categoria "BEBIDAS"
    When ler_historico é chamado para "data/order_history.json"
    Then o deve ser retornado uma lista de tamanho 1
    And a resposta deve conter um pedido com "id_historico" igual a "0001"


# ----------------------------------------------------------------
# Cenários para: Salvar Histórico
# ----------------------------------------------------------------
  Scenario: Salvar dados no histórico
    Given o caminho "data/order_history.json" é um json vazio
    When salvar_historico é chamado para "data/order_history.json"
    And o payload tem o pedido com id_historico "0001", mesa "mesa_1", total 46.3, data_fechamento "2025-07-13T11:47:52.506010" e status "concluido"
    And o pedido "0001" possui um item com produto_id "B004", nome "Cerveja Heineken Long Neck", quantidade 3, valor_unitario 9.0 e categoria "BEBIDAS
    Then o historico tem 1 pedidos
    And o historico deve conter o pedido com id_historico "0001", mesa "mesa_1", total 46.3, data_fechamento "2025-07-13T11:47:52.506010" e status "concluido"
    And o pedido "0001" possui um item com produto_id "B004", nome "Cerveja Heineken Long Neck", quantidade 3, valor_unitario 9.0 e categoria "BEBIDAS



