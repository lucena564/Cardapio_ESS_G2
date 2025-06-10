Given o administrador está visualizando a "aba inicial do cardápio".
When o administrador clica na opção "Adicionar Novo Item".
Then um modal intitulado "Adicionar Novo Item" aparece sobre a tela do cardápio.
And dentro do modal, o administrador preenche o formulário com nome, descrição, preço, categoria, e confirma.
And o novo item "Hamburguer" é registrado.
And o modal é fechado.
And ao visualizar o cardápio novamente (ou a lista é atualizada), o item aparece na categoria.