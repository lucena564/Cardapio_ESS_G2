<template>
  <div class="container">
    <div class="cardapio">
        <h2>Cardápio</h2>
        <hr class="divisoria" />

        <div class="tabs">
        <a href="/cardapio/pizzas" class="tab">Pizzas</a>
        <a href="/cardapio/lanches" class="tab">Lanches</a>
        <a href="/cardapio/bebidas" class="tab active">Bebidas</a>
        <a href="/cardapio/doces" class="tab">Doces</a>
        </div>

      <!-- <h3 class="categoria">Bebidas</h3> -->
      <button class="btn add-item">Adicionar Item</button>


      <div class="item" v-for="(produto, index) in produtos" :key="produto.ID">
        <div class="info-produto">
            <h3 class="produto_do_cardapio">{{ produto.NOME }}</h3>
            <p class="produto_do_cardapio">{{ produto.DESCRICAO }}</p>
            <span>R$ {{ produto.PRECO.toFixed(2) }}</span>
        </div>
        <div class="quantidade">
            <button @click="alterarQuantidade(index, -1)">-</button>
            <input type="number" min="0" :value="produto.quantidade" readonly />
            <button @click="alterarQuantidade(index, 1)">+</button>
        </div>
      </div>

      <div class="botoes">
        <button class="btn">Fazer Pedido</button>
        <button class="btn">Cancelar Pedido</button>
        <button class="btn">Editar Pedido</button>
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
      const res = await fetch('/dados.json');
      const json = await res.json();

      // adiciona quantidade = 0 a cada produto
      this.produtos = json.produtos
        .filter(p => p.CATEGORIA === 'BEBIDAS')
        .map(p => ({ ...p, quantidade: 0 }));
    } catch (err) {
      console.error('Erro ao carregar os dados:', err);
    }
  },
  methods: {
    alterarQuantidade(index, delta) {
      const produto = this.produtos[index];
      const novaQuantidade = produto.quantidade + delta;
      produto.quantidade = novaQuantidade < 0 ? 0 : novaQuantidade;
    }
  }
};
</script>

<style scoped>
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
  min-height: 120px; /* define uma altura mínima consistente */
  width: 100%;       /* ocupa toda a largura disponível */
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
  gap: 1.0rem;
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
  padding: 0;               /* remove preenchimentos que desalinhariam */
  text-align: center;       /* centraliza horizontalmente o texto */
  line-height: 32px;        /* alinha verticalmente o texto no centro */
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  color: #333;
  box-sizing: border-box;   /* garante que padding não aumente o tamanho */
}

.quantidade input::-webkit-inner-spin-button,
.quantidade input::-webkit-outer-spin-button {
  -webkit-appearance: none; /* remove setinhas padrão no Chrome/Safari */
  margin: 0;
}

.botoes {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  gap: 1rem;
}

.btn {
  background-color: #4CAF50; /* Verde bonito */
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

/* Estilo específico para o botão "Cancelar Pedido" */
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
  transform: scale(2);       /* dobra o tamanho */
  transform-origin: top center;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.tab {
  padding: 0.8rem 2rem;              /* 🔹 aumenta altura e largura */
  background: #f9d5d5;
  border-radius: 12px;
  text-decoration: none;
  font-size: 1.1rem;                 /* 🔹 fonte um pouco maior */
  font-weight: 500;
  color: #333;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  min-width: 120px;                  /* 🔹 força largura mínima para esticar */
  text-align: center;               /* 🔹 centraliza o texto */
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
  box-shadow: 0 0 0 2px rgba(69, 160, 73, 0.3); /* 🔹 leve destaque ao redor */
}

.categoria {
  font-size: 1.5rem;
  font-style: italic;
  margin-bottom: 1.5rem;
  color: #444;
  text-align: center;
}

.add-item {
  align-self: flex-end;
  margin-bottom: 1.5rem;
}

.divisoria {
  width: 100%;
  max-width: 3300px;
  border: none;
  border-top: 3px solid #444;
  margin: 2rem auto 3rem auto;  /* espaçamento acima e abaixo */
  border-radius: 999px;         /* arredondamento para suavizar */
}

</style>

