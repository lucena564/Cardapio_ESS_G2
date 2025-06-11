Feature: Alterando quantidade dos itens do carrinho

  Scenario: Adicionando mais um item ja existente no carrinho de compras
    Given estou na tela "Carrinho de Compras"
    And eu vejo apenas o item "Cheeseburguer" no carrinho, com preco "20.00" e quantidade "2"
    And eu vejo o valor total da compra como "40.00"
    When eu seleciono para adicionar mais um "Cheeseburguer"
    Then eu vejo a quantidade de "Cheeseburguer" no carrinho como "3"
    And And eu vejo o valor total da compra como "60.00"

  Scenario: Removendo uma unidade de item no carrinho de compras
    Given estou na tela "Carrinho de Compras"
    And eu vejo apenas o item "Cheeseburguer" no carrinho, com preco "R$20.00" e quantidade "2"
    And eu vejo o valor total da compra como "R$40.00"
    When eu seleciono para adicionar mais um "Cheeseburguer"
    Then eu vejo a quantidade de "Cheeseburguer" no carrinho como "3"
    And And eu vejo o valor total da compra como "R$60.00"

  Scenario: Removendo ultima unidade de um item no carrinho de compras
    Given estou na tela "Carrinho de Compras"
    And eu vejo apenas os itens "Hamburguer" e "Batata Frita" na lista do carrinho
    And eu vejo o preco de "Hamburguer" no carrinho como "R$20.00" e quantidade "1"
    And eu vejo o preco de "Batata Frita" no carrinho como "R$5.00" e quantidade "2"
    And eu vejo o valor total da compra como "R$30.00"
    When eu seleciono para remover um "Cheeseburguer"
    Then eu posso ver uma mensagem de confirmacao
    And eu vejo que "Cheeseburguer" foi removido do carrinho de compras
    And eu vejo o valor total da compra como "R$10.00"