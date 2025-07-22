<template>
  <div class="historico-container">
    <h1>Histórico de Pedidos</h1>
    <p>Exibindo histórico para a <strong>mesa_1</strong>.</p>

    <div v-if="carregando" class="loading">
      Buscando dados do servidor... ⏳
    </div>

    <div v-else-if="erro" class="error">
      <strong>Ocorreu um erro:</strong> {{ erro }}
    </div>

    <div v-else-if="pedidos.length === 0" class="empty">
      Nenhum pedido encontrado no histórico para esta mesa.
    </div>

    <ul v-else class="lista-pedidos">
      <li
        v-for="pedido in pedidos"
        :key="pedido.id_historico"
        class="pedido-item"
      >
        <div class="pedido-header">
          <strong>Pedido #{{ pedido.id_historico }}</strong>
          <span>{{
            new Date(pedido.data_fechamento).toLocaleString("pt-BR")
          }}</span>
          <span :class="['status', pedido.status]">{{ pedido.status }}</span>
        </div>

        <div class="pedido-body">
          <p class="itens-titulo">Itens do Pedido:</p>
          <ul class="itens-lista">
            <li
              v-for="item in pedido.itens"
              :key="item.produto_id"
              class="item"
            >
              <span class="item-quantidade">{{ item.quantidade }}x </span>
              <span class="item-nome">{{ item.nome }}</span>
            </li>
          </ul>
        </div>

        <div class="pedido-footer">
          <span> Total: R$ {{ pedido.total.toFixed(2) }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useApiService } from "../services/apiService";
import type { PedidoHistorico } from "../services/apiService";

const { getHistoricoPorMesa } = useApiService();

const pedidos = ref<PedidoHistorico[]>([]);
const carregando = ref(true);
const erro = ref<string | null>(null);

onMounted(async () => {
  try {
    pedidos.value = await getHistoricoPorMesa("mesa_1");
  } catch (err) {
    console.error("Falha ao buscar histórico:", err);
    erro.value =
      "Não foi possível conectar ao servidor para buscar o histórico.";
  } finally {
    carregando.value = false;
  }
});
</script>

<style scoped>
.historico-container {
  padding: 1rem;
  width: 200%;
  max-width: 1200px; /* ADICIONADO: Define uma largura máxima */
  margin: 0 auto; /* ADICIONADO: Centraliza o container na página */
  text-align: center; /* <-- ADICIONE ESTA LINHA */
}
.loading,
.error,
.empty {
  margin-top: 2rem;
  font-size: 1.2rem;
  text-align: center;
}
.error {
  color: #d9534f;
}
.lista-pedidos {
  list-style: none;
  padding: 0;
  margin-top: 1.5rem;
  gap: 1.5rem;
}
.pedido-item {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: var(--color-background-soft);
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
.pedido-item:hover {
  transform: translateY(-5px); /* Levanta o card um pouco */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); /* Adiciona uma sombra mais pronunciada */
}
.pedido-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}
.pedido-body {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.9rem;
  color: var(--color-text-mute);
}
.pedido-footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: var(--color-text-mute);
  margin-top: 0.5rem;
  margin-left: 1000px;
}
.status {
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: capitalize;
}
.status.concluido {
  background-color: #2f9c4c;
  color: white;
}
.status.em.andamento {
  /* Classe gerada para 'em andamento' */
  background-color: #f0ad4e;
  color: white;
}
.status.cancelado {
  background-color: #d9534f;
  color: white;
}
</style>
