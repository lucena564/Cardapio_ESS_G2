Given estou na página do cardápio digital como cliente
When adiciono o item "Hambúrguer Artesanal" de "20" reais ao carrinho 
And adiciono o item "Suco de Laranja Natural" de "10" reais ao carrinho 
Then o carrinho deve o pedido 1 com 2 itens
And o total do pedido deve ser exibido corretamente