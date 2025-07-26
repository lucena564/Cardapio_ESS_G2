<template>
  <div class="container">
    <div class="cardapio">
      <h1 class="titulo-restaurante">Bem-vindo ao Restaurante Delícia!</h1>
      <p class="subtitulo">Escolha sua mesa e veja nosso cardápio completo.</p>

      <!-- Seleção da Mesa -->
      <div class="selecao-mesa">
        <label for="mesa">Informe sua mesa:</label>
        <select id="mesa" v-model="mesaSelecionada" @change="salvarMesa">
          <option disabled value="">Selecione...</option>
          <option v-for="n in 5" :key="n" :value="`Mesa ${n}`">Mesa {{ n }}</option>
        </select>
      </div>

      <!-- Navegação de Categorias -->
      <button class="btn-categorias" @click="irParaCategorias">Ver Categorias</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mesaSelecionada: ''
    };
  },
  created() {
    const mesaSalva = localStorage.getItem('mesa');
    if (mesaSalva) this.mesaSelecionada = mesaSalva;
  },
  methods: {
    salvarMesa() {
      localStorage.setItem('mesa', this.mesaSelecionada);
    },
    irParaCategorias() {
      if (!this.mesaSelecionada) {
        alert('Por favor, selecione sua mesa antes de continuar.');
        return;
      }
      this.$router.push('/cardapio/bebidas'); // ou a categoria padrão que desejar
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
  background: #f5f5f5;
  padding: 2rem;
}

.cardapio {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 100%;
  max-width: 600px;
  font-family: 'Poppins', sans-serif;
}

.titulo-restaurante {
  font-size: 2.4rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.subtitulo {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: #555;
}

.selecao-mesa {
  margin-bottom: 2rem;
}

.selecao-mesa label {
  font-weight: 500;
  margin-right: 0.5rem;
}

.selecao-mesa select {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.btn-categorias {
  padding: 0.8rem 1.5rem;
  background-color: #27ae60;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-categorias:hover {
  background-color: #219150;
}
</style>
