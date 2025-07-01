Cenário 4: Administrador define um item existente como promocional através do modal de edição.

    Given o administrador está visualizando a "aba inicial do cardápio".
    And o administrador localiza o item "Café Espresso Duplo" com preço "R$ 10,00".
    And junto ao item, uma opção "Editar" está visível.
    When o administrador clica na opção "Editar" do item "Café Espresso Duplo".
    Then um modal intitulado "Editar Item: Café Espresso Duplo" aparece com os dados do item.
    And dentro do modal, na seção de edição, o administrador marca a opção "Ativar Promoção".
    And preenche o campo "Preço Promocional" com "R$ 8,00".
    And clica no botão "Salvar Alterações" dentro do modal.
    Then o item "Café Espresso Duplo" é atualizado com os dados da promoção.
    And o modal é fechado.
    And o sistema exibe "Promoção aplicada ao item 'Café Espresso Duplo'!".
    And no cardápio, "Café Espresso Duplo" aparece destacado ou com o preço promocional.