Background:
Given estou autenticado como cliente
 And estou na página de checkout com produtos no carrinho e endereço preenchido


scenario: pagamento

Scenario: Selecionar método de pagamento

When acesso a seção "Forma de Pagamento"
 And escolho a opção "Cartão de Crédito"
 Then o sistema deve exibir os campos para preenchimento dos dados do cartão
 And deve habilitar o botão "Finalizar Pedido"

Scenario: Realizar pagamento com cartão válido

When preencho os dados do cartão corretamente
 And clico em "Finalizar Pedido"
 Then o sistema deve processar o pagamento
 And deve exibir a mensagem "Pedido confirmado!"
 And deve mostrar o tempo estimado de entrega

Scenario: Tentar finalizar pagamento com cartão inválido

When preencho os dados do cartão com número incorreto
 And clico em "Finalizar Pedido"
 Then o sistema deve exibir a mensagem de erro "Pagamento recusado. Verifique os dados e tente novamente."

Scenario: Escolher pagamento na entrega

When escolho a opção "Pagamento na Entrega"
 Then o sistema deve exibir a mensagem "Você pagará no momento da entrega"
 And o botão "Finalizar Pedido" deve estar habilitado

Scenario: Cancelar um pedido já pago
gi
When acesso a tela de "Meus Pedidos"
 And seleciono um pedido já confirmado com pagamento online
 And clico em "Cancelar Pedido"
 Then o sistema deve exibir a mensagem "Pedido cancelado com sucesso"
 And deve iniciar o processo de reembolso automático