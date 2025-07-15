Feature: Gerenciamento de Categorias do cardápio
  Como um administrador do restaurante
  Eu quero gerenciar categorias de produtos
  Para que eu possa organizar os produtos do meu cardápio

  Scenario: Adicionar uma nova categoria
    Given não há categoria com nome "SOBREMESAS"
    When crio uma nova categoria com nome "SOBREMESAS"
    Then a categoria "SOBREMESAS" deve estar presente na lista

  Scenario: Impedir criação de categoria com nome duplicado
    Given já existe uma categoria chamada "BEBIDAS"
    When crio uma nova categoria com nome "BEBIDAS"
    Then o sistema deve exibir uma mensagem de erro indicando que a categoria já existe
    And a categoria "BEBIDAS" deve estar presente na lista

  Scenario: Impedir criação de nova categoria sem informar um nome
    When crio uma nova categoria sem informar um nome
    Then o sistema deve exibir uma mensagem de erro indicando que o nome é obrigatório
    And a categoria '' não deve estar presente na lista

  Scenario: Excluir uma categoria existente
    Given já existe uma categoria chamada "SOBREMESAS"
    When excluo a categoria "SOBREMESAS"
    Then o sistema deve exibir uma mensagem de sucesso indicando que a categoria foi excluída
    And a categoria "SOBREMESAS" não deve estar presente na lista

  Scenario: Impedir exclusão de categoria inexistente
    Given não há categoria com nome "FRUTOS DO MAR"
    When excluo a categoria "FRUTOS DO MAR"
    Then o sistema deve exibir uma mensagem de erro indicando que a categoria não foi encontrada
    And a categoria "FRUTOS DO MAR" não deve estar presente na lista

  Scenario: Atualizar o nome de uma categoria existente
    Given já existe uma categoria chamada "PIZZAS"
    When atualizo o nome da categoria de "PIZZAS" para "MASSAS"
    Then a categoria "PIZZAS" não deve estar presente na lista
    And a categoria "MASSAS" deve estar presente na lista

  Scenario: Impedir atualização de categoria inexistente
    Given não há categoria com nome "SALADAS"
    When atualizo o nome da categoria de "SALADAS" para "PRATOS VEGANOS"
    Then o sistema deve exibir uma mensagem de erro indicando que a categoria não foi encontrada
    And a categoria "PRATOS VEGANOS" não deve estar presente na lista