Feature: Sugestao de Pedidos
 
  Scenario: Excluindo uma sugestao das combinacoes
    Given estou logado como admin
    And a sugestao "ComboLancheBatata" esteja cadastrada no sistema com items "L001" e "O001"
    When eu seleciono para excluir a sugestao "ComboLancheBatata"
    Then a sugestao foi excluida com sucesso
    And a sugestao "ComboLancheBatata" nao deve mais existir no sistema