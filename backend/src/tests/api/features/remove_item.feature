Feature: Manutenção do Cardápio

  Scenario: Administrador remove um item existente
    Given que o item "Suco de Laranja" já existe no sistema
    When o administrador decide remover o item "Suco de Laranja"
    Then a remoção deve ser bem-sucedida
    And o item "Suco de Laranja" não deve mais ser encontrado no cardápio