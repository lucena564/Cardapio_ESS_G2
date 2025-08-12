<template>
  <div class="cardapio">
    <h2>{{ categoria }}</h2>
    <hr class="divisoria" />

    <CategoryTabs
      :categories="categoryStore.categories"
      :activeCategory="$route.params.categoria"
    />

    <ProductList
      :produtos="produtos"
      :itens="pedidoStore.itens"
      @alterar="alterarQuantidade"
    />

    <ActionButtons
      :pedidoEnviado="pedidoEnviado"
      @fazer-pedido="fazerPedido"
      @ir-historico="irParaHistorico"
      @cancelar="pedidoStore.zerarPedido"
    />
  </div>
</template>

<script>
import CategoryTabs from "@/components/CategoryTabs.vue";
import ProductList from "@/components/ProductList.vue";
import ActionButtons from "@/components/ActionButtons.vue";

import { usePedidoStore } from "@/stores/pedido";
import { useCategoryStore } from "@/stores/categoryStore";
import { useApiService } from "@/services/apiService";

export default {
  components: { CategoryTabs, ProductList, ActionButtons },
  data() {
    return {
      produtos: [],
      categoria: "",
      pedidoEnviado: false,
    };
  },
  computed: {
    pedidoStore: () => usePedidoStore(),
    categoryStore: () => useCategoryStore()
  },
  async created() {
    const { getPublicItems } = useApiService();
    await this.categoryStore.fetchCategories();

    try {
      this.categoria = this.$route.params.categoria.toUpperCase();
      const todosOsProdutos = await getPublicItems();
      this.produtos = todosOsProdutos.filter(
        (p) => p.CATEGORIA === this.categoria
      );
    } catch (err) {
      console.error("Erro ao carregar produtos:", err);
    }
  },
  methods: {
    alterarQuantidade(id, delta) {
      this.pedidoStore.alterarQuantidade(id, delta);
    },
    async fazerPedido() {
      const itens = Object.entries(this.pedidoStore.itens)
        .filter(([_, qtd]) => qtd > 0)
        .map(([id, qtd]) => ({ produto_id: id, quantidade: qtd }));

      if (!itens.length) {
        alert("Selecione ao menos um produto.");
        return;
      }

      try {
        await fetch(`http://localhost:8000/pedidos`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ mesa: this.pedidoStore.mesa, itens }),
        });

        this.pedidoEnviado = true;
        this.pedidoStore.zerarPedido();
        setTimeout(() => (this.pedidoEnviado = false), 3000);
      } catch (err) {
        console.error("Erro ao enviar pedido:", err);
      }
    },
    async irParaHistorico() {
      const mesa = this.pedidoStore.mesa;
      if (!mesa) return alert("Nenhuma mesa selecionada.");

      if (!confirm(`Deseja fechar os pedidos da ${mesa}?`)) return;

      try {
        const resp = await fetch(
          `http://localhost:8000/pedidos/fechar/${mesa}`,
          { method: "POST" }
        );
        if (!resp.ok) throw new Error("Falha ao fechar o pedido.");
        this.pedidoStore.zerarPedido();
        this.$router.push("/historico");
      } catch (err) {
        alert(`Erro: ${err.message}`);
      }
    }
  }
};
</script>
