Feature: Manutenção do Cardápio

  Scenario: Administrador atualiza o preço de um item existente
    Given que o item "Pizza Margherita" já existe no sistema com o preço de "35.00"
    When o administrador decide atualizar o preço do item "Pizza Margherita" para "37.50"
    Then a atualização deve ser bem-sucedida
    And o item "Pizza Margherita" deve agora custar "37.50"