<template>
  <div class="toast-container">
    <div
      v-for="message in messages"
      :key="message.id"
      :class="['toast', message.type]"
    >
      <span>{{ message.text }}</span>
      <button @click="removeMessage(message.id)" class="toast-close">×</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['remove-message'])

const removeMessage = (id) => {
  emit('remove-message', id)
}

// Auto-dismiss messages after 5 seconds
const autoDismissTimers = new Map()

onMounted(() => {
  props.messages.forEach(message => {
    if (!autoDismissTimers.has(message.id)) {
      const timer = setTimeout(() => {
        removeMessage(message.id)
        autoDismissTimers.delete(message.id)
      }, 5000)
      autoDismissTimers.set(message.id, timer)
    }
  })
})

onUnmounted(() => {
  autoDismissTimers.forEach(timer => clearTimeout(timer))
  autoDismissTimers.clear()
})
</script>

