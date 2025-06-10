Given estou na página do cardápio digital como cliente
  And já foi feito pedido que ainda não foi finalizado
  When clico em "Cancelar Pedido"
  Then aparece uma tela com os “Pedidos Realizados”
  And o usuário seleciona o pedido que deseja cancelar
  Then o pedido deve ser cancelado com sucesso
  And o carrinho deve tirar esse pedido
  And o total do pedido deve ser recalculado