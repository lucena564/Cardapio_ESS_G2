Cenários:

Background:

Given estou autenticado como cliente "joao@email.com"
And estou na página de pedidos do restaurante "Massa demais"

Scenario: Exibir notificação após confirmação do pedido

When finalizo o pedido com sucesso
Then o sistema deve exibir uma notificação com a mensagem "Pedido confirmado!"
And deve mostrar o código do pedido e o tempo estimado de entrega

Scenario: Exibir notificação de erro ao tentar confirmar o pedido

When tento finalizar o pedido
And ocorre um erro na comunicação com o servidor
Then o sistema deve exibir a mensagem "Erro ao confirmar o pedido. Tente novamente."

Scenario: Notificar o cliente sobre cancelamento do pedido

When o restaurante cancela o pedido
Then o sistema deve exibir uma notificação com a mensagem "Seu pedido foi cancelado pelo restaurante"
And deve exibir o motivo do cancelamento, se fornecido

