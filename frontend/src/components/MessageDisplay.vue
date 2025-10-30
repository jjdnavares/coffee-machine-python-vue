<template>
  <div class="toast-container">
    <v-alert
      v-for="message in messages"
      :key="message.id"
      :type="message.type"
      closable
      @click:close="removeMessage(message.id)"
      :timeout="5000"
      class="mb-2"
    >
      {{ message.text }}
    </v-alert>
  </div>
</template>

<script setup>
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
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 2000;
  max-width: 400px;
}

@media (max-width: 768px) {
  .toast-container {
    left: 1rem;
    right: 1rem;
    max-width: none;
  }
}
</style>
