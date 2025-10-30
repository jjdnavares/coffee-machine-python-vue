<template>
  <div class="card">
    <h2>Make Coffee</h2>
    <div class="coffee-buttons">
      <button
        @click="$emit('make-espresso')"
        :disabled="loading"
        class="btn btn-primary coffee-btn"
      >
        <span v-if="loading && currentAction === 'espresso'" class="spinner"></span>
        <div>
          <div class="coffee-name">Espresso</div>
          <div class="coffee-recipe">8g coffee, 24ml water</div>
        </div>
      </button>
      
      <button
        @click="$emit('make-double-espresso')"
        :disabled="loading"
        class="btn btn-primary coffee-btn"
      >
        <span v-if="loading && currentAction === 'double-espresso'" class="spinner"></span>
        <div>
          <div class="coffee-name">Double Espresso</div>
          <div class="coffee-recipe">16g coffee, 48ml water</div>
        </div>
      </button>
      
      <button
        @click="$emit('make-americano')"
        :disabled="loading"
        class="btn btn-primary coffee-btn"
      >
        <span v-if="loading && currentAction === 'americano'" class="spinner"></span>
        <div>
          <div class="coffee-name">Americano</div>
          <div class="coffee-recipe">16g coffee, 148ml water</div>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  status: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  },
  currentAction: {
    type: String,
    default: ''
  }
})

defineEmits(['make-espresso', 'make-double-espresso', 'make-americano'])
</script>

<style scoped>
.coffee-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.coffee-btn {
  flex-direction: column;
  min-height: 100px;
  padding: var(--spacing-lg);
}

.coffee-name {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: var(--spacing-xs);
}

.coffee-recipe {
  font-size: 0.875rem;
  opacity: 0.9;
}

h2 {
  margin-bottom: var(--spacing-lg);
  color: var(--primary-color);
}
</style>

