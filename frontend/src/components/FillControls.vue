<template>
  <div class="card">
    <h2>Fill Containers</h2>
    
    <div class="fill-section">
      <h3>Water Container</h3>
      <div class="fill-controls">
        <div class="input-group">
          <input
            v-model.number="waterAmount"
            type="number"
            min="0"
            :max="maxWaterFill"
            step="0.1"
            class="input"
            placeholder="Amount in ml"
            :disabled="loading"
          />
          <span class="unit">ml</span>
        </div>
        <button
          @click="handleFillWater"
          :disabled="!isValidWaterAmount || loading"
          class="btn btn-success"
        >
          Fill Water
        </button>
        <div v-if="waterFillWarning" class="warning">
          {{ waterFillWarning }}
        </div>
      </div>
    </div>
    
    <div class="fill-section">
      <h3>Coffee Container</h3>
      <div class="fill-controls">
        <div class="input-group">
          <input
            v-model.number="coffeeAmount"
            type="number"
            min="0"
            :max="maxCoffeeFill"
            step="0.1"
            class="input"
            placeholder="Amount in grams"
            :disabled="loading"
          />
          <span class="unit">g</span>
        </div>
        <button
          @click="handleFillCoffee"
          :disabled="!isValidCoffeeAmount || loading"
          class="btn btn-success"
        >
          Fill Coffee
        </button>
        <div v-if="coffeeFillWarning" class="warning">
          {{ coffeeFillWarning }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  status: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['fill-water', 'fill-coffee'])

const waterAmount = ref(0)
const coffeeAmount = ref(0)

const maxWaterFill = computed(() => {
  if (!props.status) return 2000
  return props.status.water_capacity - props.status.water_level
})

const maxCoffeeFill = computed(() => {
  if (!props.status) return 500
  return props.status.coffee_capacity - props.status.coffee_level
})

const isValidWaterAmount = computed(() => {
  return waterAmount.value > 0 && waterAmount.value <= maxWaterFill.value
})

const isValidCoffeeAmount = computed(() => {
  return coffeeAmount.value > 0 && coffeeAmount.value <= maxCoffeeFill.value
})

const waterFillWarning = computed(() => {
  if (!props.status || !waterAmount.value) return ''
  const remaining = maxWaterFill.value
  if (waterAmount.value > remaining) {
    return `Cannot exceed capacity. Maximum: ${remaining.toFixed(1)}ml`
  }
  if (remaining < 100) {
    return `Only ${remaining.toFixed(1)}ml remaining before full`
  }
  return ''
})

const coffeeFillWarning = computed(() => {
  if (!props.status || !coffeeAmount.value) return ''
  const remaining = maxCoffeeFill.value
  if (coffeeAmount.value > remaining) {
    return `Cannot exceed capacity. Maximum: ${remaining.toFixed(1)}g`
  }
  if (remaining < 50) {
    return `Only ${remaining.toFixed(1)}g remaining before full`
  }
  return ''
})

const handleFillWater = () => {
  if (isValidWaterAmount.value) {
    emit('fill-water', waterAmount.value)
    waterAmount.value = 0
  }
}

const handleFillCoffee = () => {
  if (isValidCoffeeAmount.value) {
    emit('fill-coffee', coffeeAmount.value)
    coffeeAmount.value = 0
  }
}
</script>

<style scoped>
.fill-section {
  margin: var(--spacing-lg) 0;
}

.fill-section:first-child {
  margin-top: 0;
}

h3 {
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
}

.fill-controls {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.input-group {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.input-group .input {
  flex: 1;
}

.unit {
  font-weight: 600;
  color: var(--text-secondary);
  min-width: 30px;
}

.warning {
  color: var(--warning-color);
  font-size: 0.875rem;
  margin-top: calc(var(--spacing-sm) * -1);
}

h2 {
  margin-bottom: var(--spacing-lg);
  color: var(--primary-color);
}
</style>

