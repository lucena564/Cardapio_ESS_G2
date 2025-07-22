<script setup lang="ts">
// O import do HelloWorld não é mais usado, então podemos removê-lo para limpeza.
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <div class="wrapper">
    <nav>
      <h1>Delivery ESS G2</h1>
      <RouterLink to="/">ToDoList</RouterLink>
      <RouterLink to="/about">About</RouterLink>
      <RouterLink to="/historico">Historico</RouterLink>
    </nav>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
/* Estilos para a navegação, agora como uma barra superior fixa */
nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;

  display: flex;
  justify-content: flex-end; /* Alinha os links à direita */
  align-items: center; /* Centraliza os links verticalmente */

  padding: 1rem 2rem; /* Adiciona espaçamento interno */
  height: 60px; /* Define uma altura fixa para a barra */

  background-color: var(--color-background);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid var(--color-border);
}

h1 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--color-text);
  align-self: center; /* Centraliza o título verticalmente */
  margin-right: auto; /* Empurra os links para a direita */
}

main {
  /* Empurra o conteúdo principal para baixo para não ficar atrás da nav fixa */
  padding-top: 80px; /* Um pouco mais que a altura da nav para dar um respiro */
}

/* Estilos dos links de navegação */
nav a {
  display: inline-block;
  padding: 0 1rem;
  font-size: 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border-left: 0;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

/* O media query pode não ser mais necessário, mas pode ser ajustado se precisar
   de um layout diferente para o menu em telas maiores. */
</style>
