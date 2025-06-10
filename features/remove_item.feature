Cenário 3: Administrador remove um item diretamente da visualização do cardápio.

    Given o administrador está visualizando a "aba inicial do cardápio".
    And o administrador localiza o item "Suco de Laranja".
    And junto ao item, uma opção "Excluir" está visível.
    When o administrador clica na opção "Excluir" do item "Suco de Laranja".
    Then um pequeno modal de confirmação aparece com a mensagem "Tem certeza que deseja excluir 'Suco de Laranja'?".
    And o administrador clica no botão "Confirmar Exclusão" no modal de confirmação.
    Then o item "Suco de Laranja" é removido.
    And o modal de confirmação é fechado.
    And o sistema exibe "Item 'Suco de Laranja' excluído com sucesso!".
    And o item "Suco de Laranja" não aparece mais no cardápio.