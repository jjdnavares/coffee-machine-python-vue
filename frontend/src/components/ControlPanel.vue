<template>
  <v-card class="pa-6" elevation="0">
    <v-card-title class="text-h5 mb-6">Make Coffee</v-card-title>
    <div class="coffee-grid">
      <v-card
        v-for="coffee in coffeeOptions"
        :key="coffee.id"
        :class="['coffee-card', { loading: loading && currentAction === coffee.id }]"
        @click="!loading && $emit(coffee.event)"
        :disabled="loading"
        elevation="0"
        hover
      >
        <div class="d-flex flex-column align-center justify-center pa-4 coffee-card-content">
          <div class="coffee-icon-wrapper" :class="{
            'espresso-cup': coffee.id === 'espresso',
            'double-espresso-cup': coffee.id === 'double-espresso',
            'smaller-cup': coffee.id === 'ristretto', 
            'larger-cup': coffee.id === 'americano' 
          }">
            <span class="coffee-icon">{{ coffee.icon }}</span>
          </div>
          <div class="text-body-1 font-weight-medium mt-2 text-center">{{ coffee.name }}</div>
          <div v-if="loading && currentAction === coffee.id" class="mt-2">
            <v-progress-circular indeterminate size="24" color="primary"></v-progress-circular>
          </div>
        </div>
      </v-card>
    </div>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

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

defineEmits(['make-espresso', 'make-double-espresso', 'make-ristretto', 'make-americano'])

const coffeeOptions = computed(() => [
  {
    id: 'espresso',
    name: 'Espresso',
    icon: '☕',
    event: 'make-espresso',
    description: '8g coffee, 24ml water'
  },
  {
    id: 'double-espresso',
    name: 'Double Espresso',
    icon: '☕☕',
    event: 'make-double-espresso',
    description: '16g coffee, 48ml water'
  },
  {
    id: 'ristretto',
    name: 'Ristretto',
    icon: '☕',
    event: 'make-ristretto',
    description: '8g coffee, 16ml water'
  },
  {
    id: 'americano',
    name: 'Americano',
    icon: '☕',
    event: 'make-americano',
    description: '16g coffee, 148ml water'
  }
])
</script>

<style scoped>
.coffee-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.coffee-card {
  border-radius: 16px !important;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 160px;
  background-color: rgba(var(--v-theme-surface), 0.6) !important;
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)) !important;
}

.coffee-card:hover:not(:disabled) {
  transform: translateY(-4px);
  background-color: rgba(var(--v-theme-surface), 0.8) !important;
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15) !important;
}

.coffee-card:active {
  transform: translateY(-2px);
}

.coffee-card:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.coffee-card.loading {
  border-color: rgb(var(--v-theme-primary)) !important;
}

.coffee-card-content {
  min-height: 160px;
}

.coffee-icon-wrapper {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.coffee-icon {
  display: block;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  line-height: 1;
}

.espresso-cup {
  font-size: 4rem !important;
  line-height: 1;
}

.double-espresso-cup {
  font-size: 3.5rem !important;
  line-height: 1;
}

.smaller-cup {
  font-size: 3rem !important;
  line-height: 1;
}

.larger-cup {
  font-size: 5rem !important;
  line-height: 1;
}

/* Dark mode adjustments */
.v-theme--dark .coffee-card {
  background-color: rgba(255, 255, 255, 0.03) !important;
}

.v-theme--dark .coffee-card:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.06) !important;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .coffee-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }
  
  .coffee-card {
    min-height: 140px;
  }
  
  .coffee-icon-wrapper {
    font-size: 3rem;
  }
}
</style>

