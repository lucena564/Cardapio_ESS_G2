
Given estou na tela "Carrinho de Compras"
And eu vejo o item sugerido "Aneis de Cebola" no valor de "5.00"
And eu vejo apenas o item "Triplo Burguer" no carrinho, com preco "28.00" e quantidade "2"
And eu vejo o valor total da compra como "56.00"
When eu seleciono para adicionar "Aneis de Cebola" ao carrinho
Then eu vejo "Aneis de Cebola" com preco "5.00" e quantidade "1" no carrinho
And eu vejo o valor total da compra como "61.00"