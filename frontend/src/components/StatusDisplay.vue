<template>
  <v-card class="pa-6">
    <v-card-title class="text-h5 mb-4">Machine Status</v-card-title>
    
    <div class="status-item">
      <div class="d-flex justify-space-between mb-2">
        <span class="font-weight-bold">Water</span>
        <span class="text-body-2">{{ formatNumber(status?.water_level || 0) }}ml / {{ formatNumber(status?.water_capacity || 0) }}ml ({{ formatNumber(status?.water_percentage || 0) }}%)</span>
      </div>
      <v-progress-linear
        :model-value="status?.water_percentage || 0"
        :color="getStatusColor(status?.water_percentage || 0)"
        height="30"
        striped
      >
        <template v-if="(status?.water_percentage || 0) > 10">
          <span class="text-white font-weight-bold">{{ formatNumber(status?.water_percentage || 0) }}%</span>
        </template>
      </v-progress-linear>
    </div>
    
    <div class="status-item">
      <div class="d-flex justify-space-between mb-2">
        <span class="font-weight-bold">Coffee</span>
        <span class="text-body-2">{{ formatNumber(status?.coffee_level || 0) }}g / {{ formatNumber(status?.coffee_capacity || 0) }}g ({{ formatNumber(status?.coffee_percentage || 0) }}%)</span>
      </div>
      <v-progress-linear
        :model-value="status?.coffee_percentage || 0"
        :color="getStatusColor(status?.coffee_percentage || 0)"
        height="30"
        striped
      >
        <template v-if="(status?.coffee_percentage || 0) > 10">
          <span class="text-white font-weight-bold">{{ formatNumber(status?.coffee_percentage || 0) }}%</span>
        </template>
      </v-progress-linear>
    </div>
    
    <v-divider class="my-4"></v-divider>
    
    <div class="d-flex justify-space-between align-center">
      <p class="text-body-1"><strong>Total Coffees Made:</strong> {{ status?.total_coffees_made || 0 }}</p>
      <v-btn @click="$emit('refresh-status')" color="primary">Refresh</v-btn>
    </div>
  </v-card>
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
  margin: 1.5rem 0;
}
</style>

