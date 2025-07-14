Feature: Funcionalidade de Pedido de Itens

  Scenario: Adicionar dois itens ao pedido e verificar o total
    Given estou na página do cardápio digital como cliente na "mesa_1"
    When adiciono o item "P001" com "1" quantidade(s), totalizando "45" reais ao carrinho
    And adiciono o item "P002" com "2" quantidade(s), totalizando "100" reais ao carrinho
    Then o pedido deve ser criado com sucesso