<template>
  <div class="tabs">
    <a
      v-for="cat in categories"
      :key="cat"
      :href="`/cardapio/${cat.toLowerCase()}`"
      :class="['tab', { active: cat.toLowerCase() === activeCategory }]"
    >
      {{ cat }}
    </a>
  </div>
</template>

<script>
export default {
  props: {
    categories: { type: Array, required: true },
    activeCategory: { type: String, required: true }
  }
};
</script>
