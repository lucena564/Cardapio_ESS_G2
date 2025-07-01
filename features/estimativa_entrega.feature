Cenários:

Background:

Given estou autenticado como cliente "joao@email.com"
And estou na página de pedidos do restaurante "Massa demais"


-Scenario: Mostrar estimativa de entrega após o pedido ser finalizado

When finalizo o pedido com os itens do carrinho
Then o sistema deve exibir a mensagem "Entrega estimada em 30 minutos"
And a hora prevista de entrega deve ser calculada com base na hora atual

-Scenario: Exibir estimativa de entrega antes de confirmar o pedido

When visualizo o carrinho com todos os produtos
And endereço preenchido
Then o sistema deve exibir a mensagem "Entrega estimada em 40 minutos"

-Scenario: Exibir cronômetro de entrega simples após confirmação

When finalizo o pedido
Then o sistema deve iniciar um cronômetro com base no tempo estimado
And o tempo restante deve ser exibido de forma decrescente localmente

