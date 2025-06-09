Feature: Categories
Como um administrador do restaurante
Eu quero gerenciar categorias de produtos
Para que eu possa organizar os produtos do meu cardápio

    Background: 
        Given eu estou logado como administrador
        And eu estou na página de gerenciamento de categorias
    
    Scenario: Adicionar uma nova categoria
    Given não há categoria com nome "Sobremesas" 
    When crio uma nova categoria 
    And preencho o nome como "Sobremesas" e a categoria é salva com sucesso
    Then a nova categoria "Sobremesas" deve aparecer listada e as outras categorias devem permanecer inalteradas

    Scenario: Impedir criação de categoria com nome duplicado
    Given já existe uma categoria chamada "Bebidas"
    When tento criar uma nova categoria com o nome "Bebidas"
    Then o sistema deve exibir uma mensagem de operação não confirmada
    And na lista de categorias, continuo vendo a categoria "Bebidas" e as outras categorias permanecem inalteradas

    Scenario: Cancelar exclusão acidental de uma categoria
    Given a categoria "Bebidas" está listada entre as existentes
    When clico em excluir ao lado da categoria "Bebidas"
    And cancelo a operação na caixa de confirmação
    Then a categoria "Bebidas" deve permanecer visível na lista
    And nenhuma mensagem de exclusão deve ser exibida
    And o sistema deve manter o estado anterior sem alterações

    Scenario: Impedir criação de nova categoria sem informar um nome
    When tento criar uma nova categoria sem informar o nome e tento salvar
    Then o sistema deve exibir uma mensagem de erro indicando que o nome é obrigatório
    And a categoria não deve ser criada
    And a lista de categorias deve permanecer inalterada

    Scenario: Excluir uma categoria existente
    Given a categoria "Sobremesas" está listada entre as existentes
    When clico em excluir ao lado da categoria "Sobremesas" e confirmo a exclusão
    Then a categoria "Sobremesas" não deve mais aparecer na lista
    And o sistema deve exibir uma mensagem de sucesso indicando que a categoria foi excluída
    And as outras categorias devem permanecer inalteradas