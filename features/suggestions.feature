Feature: Sugestao de pedidos

  Scenario: Adicionando um item sugerido no carrinho de compras
    Given estou na tela "Carrinho de Compras"
    And eu vejo o item sugerido "Aneis de Cebola" no valor de "5.00"
    And eu vejo apenas o item "Triplo Burguer" no carrinho, com preco "28.00" e quantidade "2"
    And eu vejo o valor total da compra como "56.00"
    When eu seleciono para adicionar "Aneis de Cebola" ao carrinho
    Then eu vejo "Aneis de Cebola" com preco "5.00" e quantidade "1" no carrinho
    And eu vejo o valor total da compra como "61.00"

  Scenario: Adicionando item sugerido que ja está no carrinho
    Given estou na tela "Carrinho de Compras"
    And eu vejo o item sugerido "Aneis de Cebola" no valor de "5.00"
    And eu vejo apenas os itens "Triplo Burguer" e "Aneis de Cebola" no carrinho
    And eu vejo "Triplo Burguer" com preco "28.00" e quantidade "1" no carrinho
    And eu vejo "Aneis de Cebola" com preco "5.00" e quantidade "1" no carrinho
    And eu vejo o valor total da compra como "33.00"
    When eu seleciono para adicionar "Aneis de Cebola" ao carrinho
    Then eu vejo "Aneis de Cebola" com quantidade "2" no carrinho
    And eu vejo o valor total da compra como "38.00"