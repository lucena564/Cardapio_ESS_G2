<template>
  <div class="container">
    <div class="cardapio">
      <h2>Cardápio</h2>
      <hr class="divisoria" />

      <div class="tabs">
        <a href="/cardapio/pizzas" class="tab active">Pizzas</a>
        <a href="/cardapio/lanches" class="tab">Lanches</a>
        <a href="/cardapio/bebidas" class="tab">Bebidas</a>
        <a href="/cardapio/doces" class="tab">Doces</a>
      </div>

      <!-- <h3 class="categoria">Pizzas</h3> -->
      <button class="btn add-item">Adicionar Item</button>

      <div class="item" v-for="produto in produtos" :key="produto.ID">
        <div class="info-produto">
          <h3 class="produto_do_cardapio">{{ produto.NOME }}</h3>
          <p class="produto_do_cardapio">{{ produto.DESCRICAO }}</p>
          <span>R$ {{ produto.PRECO.toFixed(2) }}</span>
        </div>
        <div class="quantidade">
          <button @click="alterarQuantidade(produto.ID, -1)">-</button>
          <input type="number" min="0" :value="pedidoStore.itens[produto.ID] || 0" readonly />
          <button @click="alterarQuantidade(produto.ID, 1)">+</button>
        </div>
      </div>

      <div class="botoes">
        <button class="btn" @click="fazerPedido">Fazer Pedido</button>

        <div v-if="pedidoEnviado" class="alert-overlay">
          <div class="alert-success">
            ✅ Pedido realizado com sucesso!
          </div>
        </div>

        <button class="btn">Cancelar Pedido</button>
        <button class="btn">Editar Pedido</button>
      </div>
    </div>
  </div>
</template>

<script>
import { usePedidoStore } from '@/stores/pedido'

export default {
  data() {
    return {
      produtos: [],
      pedidoEnviado: false
    }
  },
  created() {
    this.carregarPizzas()
  },
  computed: {
    pedidoStore() {
      return usePedidoStore()
    },
    mesaSelecionada: {
      get() {
        return this.pedidoStore.mesa
      },
      set(valor) {
        this.pedidoStore.setMesa(valor)  // <-- método que atualiza mesa e localStorage
      }
    }
  },
  methods: {
    async carregarPizzas() {
      try {
        const res = await fetch('/dados.json')
        const json = await res.json()
        this.produtos = json.produtos.filter(p => p.CATEGORIA === 'PIZZAS')
      } catch (err) {
        console.error('Erro ao carregar os dados:', err)
      }
    },

    alterarQuantidade(produtoId, delta) {
      this.pedidoStore.alterarQuantidade(produtoId, delta)
    },

    async fazerPedido() {
      const pedido = {
        mesa: this.mesaSelecionada,
        itens: Object.entries(this.pedidoStore.itens).map(([id, qtd]) => ({
          produto_id: id,
          quantidade: qtd
        }))
      }

      if (!pedido.mesa) {
        alert('Por favor, selecione a mesa antes de fazer o pedido.')
        return
      }

      if (pedido.itens.length === 0) {
        alert('Adicione pelo menos um item ao pedido.')
        return
      }

      try {
        await fetch('http://localhost:8000/pedidos', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(pedido)
        })

        this.pedidoEnviado = true
        this.pedidoStore.zerarPedido()

        setTimeout(() => {
          this.pedidoEnviado = false
        }, 2500)
      } catch (err) {
        console.error('Erro ao enviar pedido:', err)
      }
    }
  }
}
</script>

<style scoped>
/* Copie as mesmas regras CSS de Bebidas.vue aqui, para garantir o estilo igual */
/* Por exemplo: container, cardapio, tabs, tab, categoria, add-item, item, info-produto, quantidade, botoes, btn, alert-overlay, alert-success */

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background: #524f4f;
  box-sizing: border-box;
}

.cardapio {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 95vw;
  max-height: 90vh;
  width: 100%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow-y: auto;
  font-family: 'Poppins', sans-serif;
  color: #222;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.tab {
  padding: 0.8rem 2rem;
  background: #f9d5d5;
  border-radius: 12px;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  min-width: 120px;
  text-align: center;
  display: inline-block;
}

.tab:hover {
  background: #f2baba;
  transform: scale(1.05);
}

.tab.active {
  background: #d4f8d4;
  font-weight: 600;
  border-color: #45a049;
  color: #1b5e20;
  box-shadow: 0 0 0 2px rgba(69, 160, 73, 0.3);
}

.add-item {
  align-self: flex-end;
  margin-bottom: 1.5rem;
}

.item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem 1.5rem;
  margin-bottom: 1rem;
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  min-height: 120px;
  width: 100%;
  box-sizing: border-box;
}

.item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.info-produto {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.produto_do_cardapio {
  margin: 0.25rem 0;
  font-size: 1rem;
  color: #333;
}

.info-produto h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #222;
}

.info-produto span {
  font-size: 1rem;
  font-weight: bold;
  color: #27ae60;
  margin-top: 0.5rem;
}

.quantidade {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-top: 26px;
}

.quantidade button {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  background-color: #27ae60;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.quantidade button:hover {
  background-color: #219150;
}

.quantidade input {
  width: 48px;
  height: 32px;
  padding: 0;
  text-align: center;
  line-height: 32px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  color: #333;
  box-sizing: border-box;
}

.quantidade input::-webkit-inner-spin-button,
.quantidade input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.botoes {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  gap: 1rem;
}

.btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 12px 20px;
  margin: 5px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn:hover {
  background-color: #45a049;
  transform: scale(1.03);
}

.btn:nth-of-type(3) {
  background-color: #f44336;
}
.btn:nth-of-type(3):hover {
  background-color: #d32f2f;
}

.cardapio h2 {
  font-size: 2.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  text-align: center;
  transform: scale(2);
  transform-origin: top center;
}

.divisoria {
  width: 100%;
  max-width: 3300px;
  border: none;
  border-top: 3px solid #444;
  margin: 2rem auto 3rem auto;
  border-radius: 999px;
}

.alert-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  padding: 2rem 3rem;
  border-radius: 16px;
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  animation: fadeInOut 2.5s ease-in-out;
}

@keyframes fadeInOut {
  0% { opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { opacity: 0; }
}
</style>
