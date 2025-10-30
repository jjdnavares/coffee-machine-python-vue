<template>
  <v-app>
    <v-app-bar color="surface" prominent elevation="0">
      <v-app-bar-title class="d-flex align-center text-on-surface">
        <v-icon left size="large" color="primary">mdi-coffee-maker</v-icon>
        <span class="text-h5 font-weight-bold">Coffee Machine</span>
      </v-app-bar-title>
      
      <v-spacer></v-spacer>
      
      <!-- WebSocket Status -->
      <v-chip
        :color="wsStatus === 'connected' ? 'success' : wsStatus === 'reconnecting' ? 'warning' : 'error'"
        variant="flat"
        size="small"
        class="mr-4"
      >
        <v-icon start :icon="wsStatus === 'connected' ? 'mdi-wifi' : 'mdi-wifi-off'" size="small"></v-icon>
        {{ wsStatus === 'connected' ? 'Live' : wsStatus === 'reconnecting' ? 'Reconnecting...' : 'Offline' }}
      </v-chip>
      
      <!-- Dark Mode Toggle -->
      <v-btn icon="mdi-theme-light-dark" variant="text" @click="toggleTheme"></v-btn>
    </v-app-bar>

    <v-main class="position-relative">
      <v-container fluid class="pa-4">
        <CoffeeMachine @ws-status="handleWsStatus" />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTheme } from 'vuetify'
import CoffeeMachine from './components/CoffeeMachine.vue'

const theme = useTheme()
const wsStatus = ref('disconnected')

const toggleTheme = () => {
  theme.global.name.value = theme.global.name.value === 'light' ? 'dark' : 'light'
  localStorage.setItem('theme', theme.global.name.value)
}

const handleWsStatus = (status) => {
  wsStatus.value = status
}

onMounted(() => {
  // Load theme preference from localStorage
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    theme.global.name.value = savedTheme
  }
})
</script>

<style scoped>
/* Custom dark mode enhancements */
</style>

<style>
/* Material Design 3 theming improvements */

/* Consistent elevation and borders */
.v-card {
  border-radius: 12px !important;
  box-shadow: none !important;
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)) !important;
}

/* App bar - use surface color instead of primary */
.v-app-bar {
  background-color: rgb(var(--v-theme-surface)) !important;
  border-bottom: 1px solid rgb(var(--v-theme-outline)) !important;
}

/* Footer - subtle and clean */
.v-footer {
  background-color: rgb(var(--v-theme-surface)) !important;
  border-top: 1px solid rgb(var(--v-theme-outline)) !important;
}

/* Bottom navigation - Material Design 3 style */
.v-bottom-navigation {
  background-color: rgb(var(--v-theme-surface)) !important;
  border-top: 1px solid rgb(var(--v-theme-outline)) !important;
}

/* Buttons - improved styling */
.v-btn {
  border-radius: 24px !important;
  text-transform: none !important;
  font-weight: 500 !important;
  letter-spacing: 0.5px !important;
}

/* Primary buttons with proper elevation */
.v-btn--variant-elevated {
  box-shadow: 0px 1px 2px 0px rgba(0, 0, 0, 0.3), 0px 1px 3px 1px rgba(0, 0, 0, 0.15) !important;
}

.v-theme--dark .v-btn--variant-elevated {
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.5), 0px 2px 6px 1px rgba(0, 0, 0, 0.3) !important;
}

/* Progress bars with proper styling */
.v-progress-linear {
  border-radius: 4px !important;
}

/* Text fields with proper styling */
.v-text-field .v-field {
  border-radius: 4px !important;
}

/* Alerts with subtle borders */
.v-alert {
  border-radius: 12px !important;
  border: 1px solid rgb(var(--v-theme-outline)) !important;
}

/* Chips */
.v-chip {
  border-radius: 8px !important;
}

/* Container spacing */
.v-container {
  max-width: 1200px !important;
}

/* Ensure proper contrast */
.v-main {
  background-color: rgb(var(--v-theme-background)) !important;
}

/* Dark mode specific improvements */
.v-theme--dark {
  /* Improved card contrast in dark mode */
  --v-card-border-opacity: 0.15;
}

.v-theme--dark .v-card {
  background-color: rgb(var(--v-theme-surface)) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
}

/* Better text contrast in dark mode */
.v-theme--dark .text-on-surface {
  color: rgb(var(--v-theme-on-surface)) !important;
}

/* Improved button hover states in dark mode */
.v-theme--dark .v-btn:hover {
  background-color: rgba(255, 255, 255, 0.08) !important;
}

/* Better progress bar background in dark mode */
.v-theme--dark .v-progress-linear__background {
  background-color: rgba(255, 255, 255, 0.1) !important;
}
</style>
