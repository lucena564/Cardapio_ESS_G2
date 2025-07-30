import { defineStore } from 'pinia';

export const usePedidoStore = defineStore('pedido', {
  state: () => ({
    mesa: localStorage.getItem('mesa') || '',       // Lê do localStorage ou inicia com uma string vazia
    itens: {},                                      // Armazena os itens do pedido com o seu respectivo ID e quantidade
  }),
  actions: {
    setMesa(mesa) {
      this.mesa = mesa;
      localStorage.setItem('mesa', mesa);           // Armazena a mesa no localStorage
    },
    zerarPedido() {
      this.itens = {};                              // Zera os itens, mas mantém a mesa
    },
    alterarQuantidade(produtoId, delta) {
      const atual = this.itens[produtoId] || 0;
      const novoValor = atual + delta;
      if (novoValor <= 0) {
        delete this.itens[produtoId];
      } else {
        this.itens[produtoId] = novoValor;
      }
    }
  }
});
