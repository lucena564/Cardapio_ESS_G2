Cenário 1: Administrador adiciona um novo item ao cardápio

    Given o administrador está visualizando a "aba inicial do cardápio".
    And uma opção (botão/link) "Adicionar Novo Item" está visível para ele nesta tela.
    When o administrador clica na opção "Adicionar Novo Item".
    Then um modal intitulado "Adicionar Novo Item" aparece sobre a tela do cardápio.
    And dentro do modal, o administrador preenche o formulário com nome "Torta Holandesa Fatia", descrição "Deliciosa torta holandesa individual", preço "18.00", categoria "Sobremesas", e anexa uma imagem.
    And o administrador clica no botão "Salvar Item" dentro do modal.
    Then o sistema valida os dados.
    And o novo item "Torta Holandesa Fatia" é registrado.
    And o modal é fechado.
    And o sistema exibe uma mensagem de sucesso (ex: "Item 'Torta Holandesa Fatia' cadastrado com sucesso!").
    And ao visualizar o cardápio novamente (ou a lista é atualizada), o item "Torta Holandesa Fatia" aparece na categoria "Sobremesas".

Cenário 1.1: Tentativa de Cadastro de Novo Item com Dados Inválidos

    Given o administrador está visualizando a "aba inicial do cardápio".
    And o administrador abriu o modal "Adicionar Novo Item" a partir da aba inicial do cardápio.
    When o administrador preenche o formulário no modal com nome "Água Mineral", preço "ABC" (inválido), e categoria "Bebidas".
    And o administrador clica no botão "Salvar Item" dentro do modal.
    Then o sistema exibe uma mensagem de erro dentro do modal (ou próximo aos campos) como "Formato de preço inválido.".
    And o item "Água Mineral" não é adicionado ao cardápio.
    And o modal "Adicionar Novo Item" permanece aberto com os dados preenchidos para correção.