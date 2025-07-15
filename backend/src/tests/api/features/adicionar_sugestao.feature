Feature: Sugestao de Pedidos
 
  Scenario: Adicionando uma sugestao de combinacoes
    Given estou logado como admin
    And a sugestao "MistoQuenteComSuco" nao esta cadastrada no sistema
    When eu seleciono para adicionar a sugestao "MistoQuenteComSuco" com items "L003" e "B002"
    Then a sugestao foi adicionada com sucesso
    And a sugestao "MistoQuenteComSuco" deve aparecer no sistema