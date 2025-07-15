Feature: Sugestao de Pedidos
 
  Scenario: Identificando itens sugeridos de uma mesa
    Given estou logado como cliente da "mesa_1"
    And tenho apenas o item "P001" com quantidade 1 no carrinho
    And apenas esta cadastrada a sugestao "PizzaComCerveja" de items "P001" e "B004"
    When o sistema busca as sugestoes da "mesa_1"
    Then o item "B004" deve aparecer nas sugestoes