<template>
  <nav class="tab-navigation">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      @click="$emit('tab-change', tab.id)"
      :class="['tab-button', { active: activeTab === tab.id }]"
      :aria-label="tab.label"
    >
      <span class="tab-icon">{{ tab.icon }}</span>
      <span class="tab-label">{{ tab.label }}</span>
    </button>
  </nav>
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
.tab-navigation {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: var(--bg-card);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  padding: var(--spacing-sm) var(--spacing-xs);
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.tab-button {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm) var(--spacing-xs);
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: var(--radius-md);
  min-height: 60px;
  gap: var(--spacing-xs);
}

.tab-button:hover {
  background: rgba(139, 69, 19, 0.1);
}

.tab-button.active {
  color: var(--primary-color);
  background: rgba(139, 69, 19, 0.15);
}

.tab-button.active .tab-icon {
  transform: scale(1.1);
}

.tab-icon {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.tab-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Ensure content doesn't hide behind nav */
:global(.page-container) {
  padding-bottom: 80px; /* Space for bottom nav */
}
</style>

