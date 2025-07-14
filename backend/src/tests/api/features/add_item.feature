Feature: Manutenção do Cardápio

    Scenario: Administrador adiciona um novo item ao cardápio
        Given que o administrador está no cardapio
        When ele decide cadastrar "Torta Holandesa Fatia", com a descrição "Deliciosa torta holandesa individual", preço "18.00" e categoria "SOBREMESAS"
        Then o novo item "Torta Holandesa Fatia" deve ser criado com sucesso no sistema
        And o item "Torta Holandesa Fatia" deve estar disponível para consulta no cardápio