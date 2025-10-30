<template>
  <div class="tab-navigation-container">
    <!-- Footer text above navigation -->
    <div class="footer-text">
      <span class="text-caption text-on-surface">Built with FastAPI & Vue.js with Vuetify</span>
    </div>
    
    <!-- Bottom Navigation -->
    <v-bottom-navigation
      :model-value="activeTab"
      @update:model-value="$emit('tab-change', $event)"
      color="primary"
      class="tab-navigation"
    >
      <v-btn
        v-for="tab in tabs"
        :key="tab.id"
        :value="tab.id"
        :aria-label="tab.label"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-label">{{ tab.label }}</span>
      </v-btn>
    </v-bottom-navigation>
  </div>
</template>

<script setup>
const props = defineProps({
  activeTab: {
    type: String,
    required: true
  }
})

defineEmits(['tab-change'])

const tabs = [
  { id: 'make-coffee', icon: '☕', label: 'Make' },
  { id: 'status', icon: '📊', label: 'Status' },
  { id: 'fill', icon: '💧', label: 'Fill' }
]
</script>

<style scoped>
.tab-navigation-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: rgb(var(--v-theme-surface));
  border-top: 1px solid rgb(var(--v-theme-outline));
}

.footer-text {
  padding: 8px 16px;
  text-align: center;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.tab-icon {
  font-size: 1.5rem;
}

.tab-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
</style>

