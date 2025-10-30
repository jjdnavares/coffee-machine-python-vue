<template>
  <v-card class="pa-6">
    <v-card-title class="text-h5 mb-4">Fill Containers</v-card-title>
    
    <div class="fill-section">
      <h3 class="text-h6 mb-3">Water Container</h3>
      <v-text-field
        v-model.number="waterAmount"
        type="number"
        label="Amount"
        suffix="ml"
        min="0"
        :max="maxWaterFill"
        step="0.1"
        :disabled="loading"
        variant="outlined"
        class="mb-2"
      ></v-text-field>
      <v-btn
        @click="handleFillWater"
        :disabled="!isValidWaterAmount || loading"
        color="success"
        block
        size="large"
        class="mb-2"
      >
        Fill Water
      </v-btn>
      <v-alert
        v-if="waterFillWarning"
        type="warning"
        variant="tonal"
        density="compact"
      >
        {{ waterFillWarning }}
      </v-alert>
    </div>
    
    <v-divider class="my-6"></v-divider>
    
    <div class="fill-section">
      <h3 class="text-h6 mb-3">Coffee Container</h3>
      <v-text-field
        v-model.number="coffeeAmount"
        type="number"
        label="Amount"
        suffix="g"
        min="0"
        :max="maxCoffeeFill"
        step="0.1"
        :disabled="loading"
        variant="outlined"
        class="mb-2"
      ></v-text-field>
      <v-btn
        @click="handleFillCoffee"
        :disabled="!isValidCoffeeAmount || loading"
        color="success"
        block
        size="large"
        class="mb-2"
      >
        Fill Coffee
      </v-btn>
      <v-alert
        v-if="coffeeFillWarning"
        type="warning"
        variant="tonal"
        density="compact"
      >
        {{ coffeeFillWarning }}
      </v-alert>
    </div>
  </v-card>
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
  margin: 1.5rem 0;
}

.fill-section:first-child {
  margin-top: 0;
}
</style>

