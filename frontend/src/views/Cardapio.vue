<template>
  <div class="container">
    <div class="cardapio">
      <h2>Cardápio</h2>
      <div class="tabs">
        <a href="/entradas" class="tab">Entradas</a>
        <a href="/lanches" class="tab">Lanches</a>
        <a href="/bebidas" class="tab active">Bebidas</a>
        <a href="/doces" class="tab">Doces</a>
      </div>

      <h3 class="categoria">Bebidas</h3>
      <button class="add-item">Adicionar Item</button>

      <div class="item" v-for="produto in produtos" :key="produto.ID">
        <div class="info-produto">
          <h3 class="produto_do_cardapio">{{ produto.NOME }}</h3>
          <p class="produto_do_cardapio">{{ produto.DESCRICAO }}</p>
          <span>R$ {{ produto.PRECO.toFixed(2) }}</span>
        </div>
        <div class="quantidade">
          <button>-</button>
          <input type="number" min="0" value="0" />
          <button>+</button>
        </div>
      </div>

      <div class="botoes">
        <button>Fazer Pedido</button>
        <button>Cancelar Pedido</button>
        <button>Editar Pedido</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      produtos: []
    }
  },
  async created() {
    try {
      const res = await fetch('/dados.json')
      const json = await res.json()
      this.produtos = json.produtos.filter(p => p.CATEGORIA === 'BEBIDAS')
    } catch (err) {
      console.error('Erro ao carregar os dados:', err)
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background: #be3c3c;
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
}

.tabs {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.tab {
  display: inline-block;
  text-decoration: none;     /* 🔴 remove o sublinhado */
  color: inherit;            /* mantém a cor padrão do texto */
  padding: 0.5rem 1rem;
  border: none;
  background: #fdd;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
  font-family: inherit;
}
.tab {
  padding: 0.5rem 1rem;
  border: none;
  background: #fdd;
  border-radius: 8px;
  cursor: pointer;
}

.tab.active {
  background: #dfd;
  font-weight: bold;
}

.categoria {
  margin-top: 1rem;
  font-style: italic;
}

.add-item {
  align-self: flex-end;
  margin-bottom: 1rem;
}

.item {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  padding: 1rem;
  border-radius: 8px;
  width: 100%;
  box-sizing: border-box;
}

.info-produto {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.produto_do_cardapio {
  margin: 0;
}

.quantidade {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.botoes {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  gap: 1rem;
}
</style>
