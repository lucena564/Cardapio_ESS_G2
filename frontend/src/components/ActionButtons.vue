<template>
  <div class="botoes">
    <button class="btn" @click="$emit('fazer-pedido')">Adicionar</button>

    <div v-if="pedidoEnviado" class="alert-overlay">
      <div class="alert-success">✅ Pedido realizado com sucesso!</div>
    </div>

    <button class="btn" @click="$emit('ir-historico')">Enviar e Acompanhar</button>
    <button class="btn cancelar" @click="$emit('cancelar')">Cancelar Pedidos</button>
  </div>
</template>

<script>
export default {
  props: {
    pedidoEnviado: Boolean
  }
};
</script>
