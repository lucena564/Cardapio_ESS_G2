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

  Scenario: Erro na lista de sugestoes ao esvaziar carrinho
    Given estou na tela "Carrinho de Compras"
    And eu vejo apenas o item "Cheeseburguer" no carrinho, com preco "22.00" e quantidade "1"
    And eu vejo o item "Aneis de Cebola" na lista de sugestoes
    When eu seleciono para esvaziar o carrinho
    Then eu vejo que nao ha mais itens na lista de sugeridos
    And eu vejo que a lista do carrinho esta vazia
    And eu vejo o valor total da compra como "0.00"
    And eu vejo uma mensagem "Carrinho vazio. Nao ha itens para sugerir"

  Scenario: Itens no carrinho que nao geram sugestoes
    Given estou na tela "Carrinho de Compras"
    And eu vejo o item sugerido "Aneis de Cebola" no valor de "5.00"
    And eu vejo apenas os itens "Triplo Burguer" e "Refrigerante" no carrinho
    And eu vejo "Triplo Burguer" com preco "28.00" e quantidade "1" no carrinho
    And eu vejo "Refrigerante" com preco "4.00" e quantidade "1" no carrinho
    And eu vejo o valor total da compra como "32.00"
    When eu removo "Triplo Burguer" do carrinho
    Then eu vejo o valor total da compra como "28.00"
    And eu vejo que nao ha mais itens na lista de sugeridos
    And eu vejo uma mensagem "Itens do carrinho nao geram sugestoes"
    And eu vejo apenas "Refrigerante" no carrinho

  Scenario: Item sugerido indisponivel
    Given estou na tela "Carrinho de Compras"
    And eu vejo o item sugerido "Aneis de Cebola" no valor de "5.00"
    And eu vejo apenas "Triplo Burguer" com preco "28.00" e quantidade "1" no carrinho
    And eu vejo o valor total da compra como "28.00"
    And o item "Aneis de Cebola" ficou indisponivel
    When eu tento adicionar "Aneis de Cebola" ao carrinho
    Then eu vejo a mensagem "Erro. Item indisponivel no momento"