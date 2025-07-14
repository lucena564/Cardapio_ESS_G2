Feature: Gerenciamento do Histórico de Pedidos
  As a user of the system
  I want to be able to view, update, delete and filter historical orders
  To ensure data is accessible and can be managed correctly.





# ----------------------------------------------------------------
# Cenários para: GET /historico/{mesa}
# ----------------------------------------------------------------
  Scenario: Consultar com sucesso o histórico de uma mesa com pedidos existentes
    Given que existe no histórico um pedido com id_historico "0001", mesa "mesa_1", total 46.3, data_fechamento "2025-07-13T11:47:52.506010" e status "concluido"
    And o pedido "0001" possui um item com produto_id "B004", nome "Cerveja Heineken Long Neck", quantidade 3, valor_unitario 9.0 e categoria "BEBIDAS"
    And o pedido "0001" possui um item com produto_id "L001", nome "X-Burger Clássico", quantidade 1, valor_unitario 22.0 e categoria "LANCHES"
    And que existe no histórico um pedido com id_historico "0002", mesa "mesa_1", total 45.0, data_fechamento "2025-07-13T16:49:39.719517" e status "em andamento"
    And o pedido "0002" possui um item com produto_id "P001", nome "Pizza Margherita", quantidade 1, valor_unitario 45.0 e categoria "PIZZAS"
    When um cliente faz uma requisição GET para "/historico/mesa_1"
    Then o código de status da resposta deve ser 200
    And o corpo da resposta deve ser uma lista JSON contendo 2 pedidos
    And a resposta deve conter um pedido com "id_historico" igual a "0001"

  Scenario: Tentar consultar o histórico de uma mesa que não possui registros
    Given o arquivo de histórico está vazio
    When um cliente faz uma requisição GET para "/historico/mesa_3"
    Then o código de status da resposta deve ser 404
    And o corpo da resposta deve conter a mensagem de erro "Nenhum histórico encontrado para a mesa_3. Verifique se a mesa existe ou se já finalizou algum pedido."

# ----------------------------------------------------------------
# Cenários para: PUT /historico/{id_historico}
# ----------------------------------------------------------------
  Scenario: Atualizar com sucesso o status de um pedido existente
    Given que existe no histórico um pedido com id_historico "0001", mesa "mesa_1", total 45.0, data_fechamento "2025-07-13T16:49:39.719517" e status "em andamento"
    And o pedido "0001" possui um item com produto_id "P001", nome "Pizza Margherita", quantidade 1, valor_unitario 45.0 e categoria "PIZZAS"
    When um cliente faz uma requisição PUT para "/historico/0001" com o seguinte corpo: id_historico "0001", mesa "mesa_1", total 45.0, data_fechamento "2025-07-13T16:49:39.719517" e status "cancelado" e possui um item com produto_id "P001", nome "Pizza Margherita", quantidade 1, valor_unitario 45.0 e categoria "PIZZAS"
    Then o código de status da resposta deve ser 200
    And o pedido com "id_historico" "0001" no arquivo de histórico deve agora ter o status "cancelado"

  Scenario: Tentar atualizar um pedido com um ID que não existe
    Given o arquivo de histórico está vazio
    When um cliente faz uma requisição PUT para "/historico/9999" com um corpo JSON válido
    Then o código de status da resposta deve ser 404
    And o corpo da resposta deve conter a mensagem de erro "Pedido com ID 9999 não encontrado no histórico."

# ----------------------------------------------------------------
# Cenários para: DELETE /historico/
# ----------------------------------------------------------------
  Scenario: Deletar múltiplos pedidos do histórico com sucesso
    Given que existe no histórico um pedido com id_historico "0001", mesa "mesa_1", total 46.3, data_fechamento "2025-07-13T11:47:52.506010" e status "concluido"
    And o pedido "0001" possui um item com produto_id "B004", nome "Cerveja Heineken Long Neck", quantidade 3, valor_unitario 9.0 e categoria "BEBIDAS"
    And o pedido "0001" possui um item com produto_id "L001", nome "X-Burger Clássico", quantidade 1, valor_unitario 22.0 e categoria "LANCHES"
    And que existe no histórico um pedido com id_historico "0002", mesa "mesa_1", total 45.0, data_fechamento "2025-07-13T16:49:39.719517" e status "em andamento"
    And o pedido "0002" possui um item com produto_id "P001", nome "Pizza Margherita", quantidade 1, valor_unitario 45.0 e categoria "PIZZAS"
    When um cliente faz uma requisição DELETE para "/historico" com o seguinte corpo "0001 e 0003"
    Then o código de status da resposta deve ser 200
    And o corpo da resposta deve conter a mensagem "Pedidos selecionados foram removidos com sucesso."
    And o arquivo de histórico deve agora conter apenas 1 pedido
    And o arquivo de histórico não deve mais conter um pedido com "id_historico" "0001"

# ----------------------------------------------------------------
# Cenários para: GET /historico/{mesa}/filtrar
# ----------------------------------------------------------------
  Scenario: Filtrar o histórico de uma mesa por status com sucesso
    Given que existe no histórico um pedido com id_historico "0001", mesa "mesa_1", total 46.3, data_fechamento "2025-07-13T11:47:52.506010" e status "concluido"
    And o pedido "0001" possui um item com produto_id "B004", nome "Cerveja Heineken Long Neck", quantidade 3, valor_unitario 9.0 e categoria "BEBIDAS"
    And o pedido "0001" possui um item com produto_id "L001", nome "X-Burger Clássico", quantidade 1, valor_unitario 22.0 e categoria "LANCHES"
    And que existe no histórico um pedido com id_historico "0002", mesa "mesa_1", total 45.0, data_fechamento "2025-07-13T16:49:39.719517" e status "em andamento"
    And o pedido "0002" possui um item com produto_id "P001", nome "Pizza Margherita", quantidade 1, valor_unitario 45.0 e categoria "PIZZAS"
    When um cliente faz uma requisição GET para "/historico/mesa_1/filtrar?status=concluido"
    Then o código de status da resposta deve ser 200
    And o corpo da resposta deve ser uma lista JSON contendo 1 pedidos
    And todos os pedidos na resposta devem ter o status "concluido"

  Scenario: Filtrar o histórico de uma mesa por categoria e data combinados
    Given que existe no histórico um pedido com id_historico "0001", mesa "mesa_1", total 46.3, data_fechamento "2025-07-13T11:47:52.506010" e status "concluido"
    And o pedido "0001" possui um item com produto_id "B004", nome "Cerveja Heineken Long Neck", quantidade 3, valor_unitario 9.0 e categoria "BEBIDAS"
    And o pedido "0001" possui um item com produto_id "L001", nome "X-Burger Clássico", quantidade 1, valor_unitario 22.0 e categoria "LANCHES"
    And que existe no histórico um pedido com id_historico "0002", mesa "mesa_1", total 45.0, data_fechamento "2025-07-13T16:49:39.719517" e status "em andamento"
    And o pedido "0002" possui um item com produto_id "P001", nome "Pizza Margherita", quantidade 1, valor_unitario 45.0 e categoria "PIZZAS"
    When um cliente faz uma requisição GET para "/historico/mesa_1/filtrar?categoria=BEBIDAS&data=2025-07-13"
    Then o código de status da resposta deve ser 200
    And o corpo da resposta deve ser uma lista JSON contendo 1 pedidos
    And o pedido na resposta deve ter o "id_historico" "0001"

  Scenario: Realizar uma busca com filtros que não retorna nenhum resultado
    Given que existe no histórico um pedido com id_historico "0001", mesa "mesa_1", total 46.3, data_fechamento "2025-07-13T11:47:52.506010" e status "concluido"
    And o pedido "0001" possui um item com produto_id "B004", nome "Cerveja Heineken Long Neck", quantidade 3, valor_unitario 9.0 e categoria "BEBIDAS"
    And o pedido "0001" possui um item com produto_id "L001", nome "X-Burger Clássico", quantidade 1, valor_unitario 22.0 e categoria "LANCHES"
    And que existe no histórico um pedido com id_historico "0002", mesa "mesa_1", total 45.0, data_fechamento "2025-07-13T16:49:39.719517" e status "em andamento"
    And o pedido "0002" possui um item com produto_id "P001", nome "Pizza Margherita", quantidade 1, valor_unitario 45.0 e categoria "PIZZAS"
    When um cliente faz uma requisição GET para "/historico/mesa_1/filtrar?status=cancelado"
    Then o código de status da resposta deve ser 200
    And o corpo da resposta deve ser uma lista JSON vazia "[]"