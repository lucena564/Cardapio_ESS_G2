Feature: Categories
Como um administrador do restaurante
Eu quero gerenciar categorias de produtos
Para que eu possa organizar os produtos do meu cardápio

    Background: 
        Given eu estou logado como administrador
        And eu estou na página de gerenciamento de categorias
    
    Scenario: Adicionar uma nova categoria
    Given não há categoria com nome "Sobremesas" 
    When gerencio as categorias e crio uma nova categoria 
    And preencho o nome como "Sobremesas" e a categoria é salva com sucesso
    Then a nova categoria "Sobremesas" deve aparecer listada e as outras categorias devem permanecer inalteradas