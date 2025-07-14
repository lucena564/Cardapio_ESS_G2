Feature: Cancelamento de Pedido

  Scenario: Cancelar um pedido ainda não finalizado
    Given estou na página do cardápio digital como cliente
    And já foi feito um pedido que ainda não foi finalizado
    When clico em "Cancelar Pedido"
    Then deve aparecer uma tela com os "Pedidos Realizados"
    And o usuário seleciona o pedido que deseja cancelar
    Then o pedido deve ser cancelado com sucesso
    And o carrinho deve remover esse pedido
    And o total do pedido deve ser recalculado corretamente