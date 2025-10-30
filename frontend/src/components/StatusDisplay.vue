<template>
  <div class="card">
    <h2>Machine Status</h2>
    
    <div class="status-item">
      <div class="status-header">
        <span>Water</span>
        <span>{{ formatNumber(status?.water_level || 0) }}ml / {{ formatNumber(status?.water_capacity || 0) }}ml ({{ formatNumber(status?.water_percentage || 0) }}%)</span>
      </div>
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :class="getStatusColor(status?.water_percentage || 0)"
          :style="{ width: (status?.water_percentage || 0) + '%' }"
        >
          <span v-if="(status?.water_percentage || 0) > 10">{{ formatNumber(status?.water_percentage || 0) }}%</span>
        </div>
      </div>
    </div>
    
    <div class="status-item">
      <div class="status-header">
        <span>Coffee</span>
        <span>{{ formatNumber(status?.coffee_level || 0) }}g / {{ formatNumber(status?.coffee_capacity || 0) }}g ({{ formatNumber(status?.coffee_percentage || 0) }}%)</span>
      </div>
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :class="getStatusColor(status?.coffee_percentage || 0)"
          :style="{ width: (status?.coffee_percentage || 0) + '%' }"
        >
          <span v-if="(status?.coffee_percentage || 0) > 10">{{ formatNumber(status?.coffee_percentage || 0) }}%</span>
        </div>
      </div>
    </div>
    
    <div class="status-footer">
      <p><strong>Total Coffees Made:</strong> {{ status?.total_coffees_made || 0 }}</p>
      <button @click="$emit('refresh-status')" class="btn btn-primary">Refresh</button>
    </div>
  </div>
</template>

<script setup>
import { formatNumber, getStatusColor } from '../utils/helpers'

defineProps({
  status: {
    type: Object,
    default: () => ({})
  }
})

defineEmits(['refresh-status'])
</script>

<style scoped>
.status-item {
  margin: var(--spacing-lg) 0;
}

.status-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--spacing-sm);
  font-weight: 600;
}

.status-footer {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid #E0E0E0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h2 {
  margin-bottom: var(--spacing-lg);
  color: var(--primary-color);
}
</style>

