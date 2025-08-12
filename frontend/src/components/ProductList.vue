<template>
  <div class="item" v-for="produto in produtos" :key="produto.ID">
    <div class="info-produto">
      <h3>{{ produto.NOME }}</h3>
      <p>{{ produto.DESCRICAO }}</p>
      <div class="price-container">
        <span v-if="produto.DESCONTO > 0" class="original-price">
          R$ {{ produto.PRECO.toFixed(2) }}
        </span>
        <span class="final-price">
          R$ {{ calcularPrecoFinal(produto).toFixed(2) }}
        </span>
      </div>
    </div>

    <div class="quantidade">
      <button @click="$emit('alterar', produto.ID, -1)">-</button>
      <input
        type="number"
        min="0"
        :value="itens[produto.ID] || 0"
        readonly
      />
      <button @click="$emit('alterar', produto.ID, 1)">+</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    produtos: { type: Array, required: true },
    itens: { type: Object, required: true }
  },
  methods: {
    calcularPrecoFinal(produto) {
      return produto.DESCONTO > 0
        ? produto.PRECO * (1 - produto.DESCONTO / 100)
        : produto.PRECO;
    }
  }
};
</script>
