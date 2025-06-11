Feature: Alterando quantidade dos itens do carrinho

  Scenario: Adicionando mais um item ja existente no carrinho de compras
    Given estou na tela "Carrinho de Compras"
    And eu vejo apenas o item "Cheeseburguer" no carrinho, com preco "20.00" e quantidade "2"
    And eu vejo o valor total da compra como "40.00"
    When eu seleciono para adicionar mais um "Cheeseburguer"
    Then eu vejo a quantidade de "Cheeseburguer" no carrinho como "3"
    And And eu vejo o valor total da compra como "60.00"

    