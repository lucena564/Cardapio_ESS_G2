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

      <div class="item" v-for="i in 6" :key="i">
        <!-- <input placeholder="Nome" />
        <input placeholder="Descrição" /> -->
        <h3 class="produto_do_cardapio">Coca-Cola</h3>
        <p class="produto_do_cardapio">R$45</p>
        <button>Editar Item</button>
        <span>R$ 00,00</span>
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

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #be3c3c;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;         /* adiciona espaço interno para mostrar o fundo vermelho */
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
  float: right;
  margin-bottom: 1rem;
}

.item {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 1rem;
}

.item input[type="text"], .item input[placeholder] {
  flex: 1;
}

.quantidade {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.botoes {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}
</style>
