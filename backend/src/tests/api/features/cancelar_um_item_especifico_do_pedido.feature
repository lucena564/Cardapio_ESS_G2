Feature: Edição de Pedido

  Scenario: Editar um pedido removendo um item
    Given estou na página do cardápio digital como cliente
    And adiciono os itens "Suco de Laranja" de "10" reais e "X-Burger" de "20" reais
    And clico em "Fazer Pedido"
    When clico em "Editar Pedido"
    Then janela com os pedidos realizados é aberta
    And seleciono o pedido que acabou de ser computado
    And removo o item "Suco de Laranja"
    And clico em "Atualizar Pedido"
    Then o pedido deve conter apenas o item "X-Burger"
    And o total do pedido deve ser recalculado
