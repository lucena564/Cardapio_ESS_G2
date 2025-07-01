Cenário 2: Administrador atualiza um item existente através de um modal de edição.

    Given o administrador está visualizando a "aba inicial do cardápio".
    And o administrador localiza o item "Pizza Marguerita" que tem preço "R$ 35,00".
    And junto ao item "Pizza Marguerita", uma opção "Editar" está visível para o administrador.
    When o administrador clica na opção "Editar" do item "Pizza Marguerita".
    Then um modal intitulado "Editar Item: Pizza Marguerita" aparece, pré-preenchido com os dados do item.
    And dentro do modal, o administrador altera o campo "preço" para "R$ 37,50".
    And clica no botão "Salvar Alterações" dentro do modal.
    Then o item "Pizza Marguerita" é atualizado.
    And o modal é fechado.
    And o sistema exibe "Item 'Pizza Marguerita' atualizado com sucesso!".
    And na visualização do cardápio, o item "Pizza Marguerita" agora mostra o preço "R$ 37,50".