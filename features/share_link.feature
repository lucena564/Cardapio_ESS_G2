Feature: share_link
Como um administrador do restaurante
Eu quero gerar um link curto para o meu cardápio
Para que eu possa compartilhar facilmente o cardápio com clientes e parceiros

    Background:
        Given Estou logado como administrador
        And estou na página de gerenciamento do restaurante
    
    Scenario: Gerar link com sucesso
    When clico no botão para compartilhar o restaurante
    Then o sistema deve gerar um link único curto
    And o link deve ser exibido com botão de copiar
    And o link deve redirecionar para a página pública do restaurante

    Scenario: Invalidar link existente
    Given já existe um link curto gerado para o restaurante
    When clico no botão para invalidar o link existente
    Then o sistema deve invalidar o link anterior