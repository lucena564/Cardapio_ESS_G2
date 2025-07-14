Feature: Manutenção do Cardápio

  Scenario: Administrador define um item como promocional
    Given que o item "Café Espresso Duplo" existe com o preço de "10.00" e sem desconto
    When o administrador decide aplicar um desconto de "20" por cento para o item "Café Espresso Duplo"
    Then a promoção deve ser aplicada com sucesso
    And o item "Café Espresso Duplo" deve agora ter um desconto de "20" por cento