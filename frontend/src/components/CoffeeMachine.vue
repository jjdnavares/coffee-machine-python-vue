<template>
  <div class="coffee-machine-python-vue">
    <!-- Brewing Animation Overlay -->
    <v-overlay
      :model-value="loading"
      persistent
      class="brewing-overlay"
    >
      <v-card class="pa-8 text-center brewing-card" elevation="24">
        <v-progress-circular
          indeterminate
          size="80"
          width="8"
          color="primary"
          class="mb-6"
        ></v-progress-circular>
        <h2 class="text-h4 mb-2">{{ getActionName(currentAction) }}</h2>
        <p class="text-body-1 text-grey mb-2">{{ getActionMessage(currentAction) }}</p>
        <div class="text-h5 text-primary mt-2">{{ formatTime(timeRemaining) }}</div>
        <div class="mt-4">
          <div class="brewing-particles">
            <span class="particle"></span>
            <span class="particle"></span>
            <span class="particle"></span>
          </div>
        </div>
      </v-card>
    </v-overlay>
    
    <!-- Coffee Ready Modal -->
    <v-dialog
      v-model="showReadyModal"
      max-width="500"
      persistent
      class="coffee-ready-dialog"
    >
      <v-card class="pa-8 text-center coffee-ready-card" elevation="24">
        <div class="success-icon mb-4">✓</div>
        <h2 class="text-h3 mb-2 text-success">{{ readyCoffeeName }}{{ readyCoffeeName.includes('Filled') ? '!' : ' Ready!' }}</h2>
        <p class="text-body-1 text-grey mb-6" v-if="!readyCoffeeName.includes('Filled')">Your perfect cup is waiting for you ☕</p>
        <p class="text-body-1 text-grey mb-6" v-else>Container has been refilled successfully!</p>
        <v-btn
          v-if="!readyCoffeeName.includes('Filled')"
          color="primary"
          size="large"
          @click="showReadyModal = false"
          class="px-8"
        >
          Enjoy!
        </v-btn>
      </v-card>
    </v-dialog>
    
    <!-- Error Modal -->
    <v-dialog
      v-model="showErrorModal"
      max-width="500"
      persistent
      class="error-dialog"
    >
      <v-card class="pa-8 text-center error-card" elevation="24">
        <div class="error-icon mb-4">⚠️</div>
        <h2 class="text-h3 mb-2 text-error">Unable to Brew</h2>
        <p class="text-body-1 text-grey mb-6">{{ errorMessage }}</p>
        <v-btn
          color="primary"
          size="large"
          @click="showErrorModal = false"
          class="px-8"
        >
          OK
        </v-btn>
      </v-card>
    </v-dialog>
    
    <!-- Page Content based on active tab -->
    <div class="page-container">
      <!-- Make Coffee Page (Default) -->
      <div v-show="activeTab === 'make-coffee'" class="page-content">
        <ControlPanel
          :status="status"
          :loading="loading"
          :current-action="currentAction"
          @make-espresso="makeEspresso"
          @make-double-espresso="makeDoubleEspresso"
          @make-ristretto="makeRistretto"
          @make-americano="makeAmericano"
        />
        <!-- Quick status summary on make coffee page -->
        <v-card class="pa-4 mt-4">
          <div class="d-flex justify-space-around">
            <div class="text-center">
              <div class="text-caption font-weight-bold text-uppercase text-grey">Water</div>
              <div class="text-h6 font-weight-bold text-primary">{{ formatNumber(status?.water_level || 0) }}ml</div>
            </div>
            <div class="text-center">
              <div class="text-caption font-weight-bold text-uppercase text-grey">Coffee</div>
              <div class="text-h6 font-weight-bold text-primary">{{ formatNumber(status?.coffee_level || 0) }}g</div>
            </div>
          </div>
        </v-card>
      </div>
      
      <!-- Status Page -->
      <div v-show="activeTab === 'status'" class="page-content">
        <StatusDisplay :status="status" @refresh-status="fetchStatus" />
      </div>
      
      <!-- Fill Containers Page -->
      <div v-show="activeTab === 'fill'" class="page-content">
        <FillControls
          :status="status"
          :loading="loading"
          @fill-water="fillWater"
          @fill-coffee="fillCoffee"
        />
      </div>
    </div>
    
    <!-- Bottom Navigation -->
    <TabNavigation
      :active-tab="activeTab"
      @tab-change="activeTab = $event"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { coffeeAPI } from '../services/api'
import wsService from '../services/websocket'
import { formatMessage, formatNumber } from '../utils/helpers'
import StatusDisplay from './StatusDisplay.vue'
import ControlPanel from './ControlPanel.vue'
import FillControls from './FillControls.vue'
import MessageDisplay from './MessageDisplay.vue'
import TabNavigation from './TabNavigation.vue'

// Emit ws status to parent
const emit = defineEmits(['ws-status'])

// Tab management - 'make-coffee' is the default entry point
const activeTab = ref('make-coffee')

const status = ref(null)
const loading = ref(false)
const currentAction = ref('')
const messages = ref([])
const showReadyModal = ref(false)
const showErrorModal = ref(false)
const readyCoffeeName = ref('')
const errorMessage = ref('')
const timeRemaining = ref(0)
let messageIdCounter = 0
let countdownInterval = null
const wsReady = ref(false)

const addMessage = (text, type = 'info') => {
  const id = ++messageIdCounter
  messages.value.push({ id, text, type, timestamp: Date.now() })
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    removeMessage(id)
  }, 5000)
}

const removeMessage = (id) => {
  const index = messages.value.findIndex(m => m.id === id)
  if (index > -1) {
    messages.value.splice(index, 1)
  }
}

const handleError = (error) => {
  console.error('Error:', error)
  const errorMessage = error.response?.data?.message || error.message || 'An error occurred'
  addMessage(errorMessage, 'error')
}

const fetchStatus = async () => {
  try {
    loading.value = true
    const response = await coffeeAPI.getStatus()
    if (response.data.success && !wsReady.value) {
      status.value = response.data.data
    }
  } catch (error) {
    handleError(error)
  } finally {
    loading.value = false
  }
}

const getBrewingTime = (type) => {
  // Demo brewing times (half of standard) in milliseconds
  const times = {
    'espresso': 12500,      // 12.5 seconds
    'double-espresso': 15000, // 15 seconds
    'ristretto': 10000,     // 10 seconds (shorter, more concentrated)
    'americano': 17500      // 17.5 seconds (longer extraction + hot water)
  }
  return times[type] || 12500
}

const startCountdown = (duration) => {
  timeRemaining.value = duration
  if (countdownInterval) clearInterval(countdownInterval)
  
  countdownInterval = setInterval(() => {
    timeRemaining.value--
    if (timeRemaining.value <= 0) {
      clearInterval(countdownInterval)
    }
  }, 1000)
}

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const makeCoffee = async (type, actionName) => {
  try {
    loading.value = true
    currentAction.value = actionName
    
    // Get brewing time based on coffee type
    const brewingTime = getBrewingTime(type)
    const brewingTimeSeconds = Math.ceil(brewingTime / 1000)
    
    // Start countdown timer
    startCountdown(brewingTimeSeconds)
    
    const brewingPromise = new Promise(resolve => setTimeout(resolve, brewingTime))
    
    // Make the API call
    let apiPromise
    switch (type) {
      case 'espresso':
        apiPromise = coffeeAPI.makeEspresso()
        break
      case 'double-espresso':
        apiPromise = coffeeAPI.makeDoubleEspresso()
        break
      case 'ristretto':
        apiPromise = coffeeAPI.makeRistretto()
        break
      case 'americano':
        apiPromise = coffeeAPI.makeAmericano()
        break
    }
    
    // Wait for both brewing animation and API call
    const [response] = await Promise.all([apiPromise, brewingPromise])
    
    // Always refresh status after operation (success or error)
    await fetchStatus()
    
    if (response.data.success) {
      // Show coffee ready modal
      readyCoffeeName.value = getCoffeeName(actionName)
      showReadyModal.value = true
      
      // Auto close after 3 seconds
      setTimeout(() => {
        showReadyModal.value = false
      }, 3000)
    }
    } catch (error) {
    handleError(error)
    
    // Always refresh status even on error to get latest state
    await fetchStatus()
    
    // Show error modal for coffee making errors
    if (error.response?.status === 409) {
      const errorMsg = error.response?.data?.message || 'Insufficient resources to make coffee'
      errorMessage.value = errorMsg
      showErrorModal.value = true
      
      // Auto close after 4 seconds
      setTimeout(() => {
        showErrorModal.value = false
      }, 4000)
    }
  } finally {
    loading.value = false
    currentAction.value = ''
  }
}

const makeEspresso = () => makeCoffee('espresso', 'espresso')
const makeDoubleEspresso = () => makeCoffee('double-espresso', 'double-espresso')
const makeRistretto = () => makeCoffee('ristretto', 'ristretto')
const makeAmericano = () => makeCoffee('americano', 'americano')

const getCoffeeName = (action) => {
  const names = {
    'espresso': 'Espresso',
    'double-espresso': 'Double Espresso',
    'ristretto': 'Ristretto',
    'americano': 'Americano'
  }
  return names[action] || 'Coffee'
}

const getActionName = (action) => {
  const names = {
    'filling-water': 'Filling Water',
    'filling-coffee': 'Filling Coffee',
  }
  return names[action] || getCoffeeName(action)
}

const getActionMessage = (action) => {
  const messages = {
    'filling-water': 'Adding water to container... 💧',
    'filling-coffee': 'Adding coffee to container... ☕',
  }
  return messages[action] || 'Brewing your perfect cup... ☕'
}

const fillWater = async (amount) => {
  try {
    loading.value = true
    currentAction.value = 'filling-water'
    
    // Simulate filling time
    const fillingTime = 5000 // 5 seconds
    startCountdown(5)
    
    const fillingPromise = new Promise(resolve => setTimeout(resolve, fillingTime))
    
    // Make the API call
    const apiPromise = coffeeAPI.fillWater(amount)
    
    // Wait for both filling animation and API call
    const [response] = await Promise.all([apiPromise, fillingPromise])
    
    // Always refresh status after operation
    await fetchStatus()
    
    if (response.data.success) {
      // Show success modal
      readyCoffeeName.value = 'Water Filled'
      showReadyModal.value = true
      
      // Auto close after 2 seconds
      setTimeout(() => {
        showReadyModal.value = false
      }, 2000)
    }
  } catch (error) {
    handleError(error)
    // Refresh status even on error
    await fetchStatus()
  } finally {
    loading.value = false
    currentAction.value = ''
  }
}

const fillCoffee = async (amount) => {
  try {
    loading.value = true
    currentAction.value = 'filling-coffee'
    
    // Simulate filling time
    const fillingTime = 5000 // 5 seconds
    startCountdown(5)
    
    const fillingPromise = new Promise(resolve => setTimeout(resolve, fillingTime))
    
    // Make the API call
    const apiPromise = coffeeAPI.fillCoffee(amount)
    
    // Wait for both filling animation and API call
    const [response] = await Promise.all([apiPromise, fillingPromise])
    
    // Always refresh status after operation
    await fetchStatus()
    
    if (response.data.success) {
      // Show success modal
      readyCoffeeName.value = 'Coffee Filled'
      showReadyModal.value = true
      
      // Auto close after 2 seconds
      setTimeout(() => {
        showReadyModal.value = false
      }, 2000)
    }
  } catch (error) {
    handleError(error)
    // Refresh status even on error
    await fetchStatus()
  } finally {
    loading.value = false
    currentAction.value = ''
  }
}

const handleConnected = () => { wsReady.value = true; emit('ws-status', 'connected') }
const handleDisconnected = () => { wsReady.value = false; emit('ws-status', 'disconnected') }
const handleStatusUpdate = (message) => { if (message.data) status.value = message.data }
const handleCoffeeMade = (message) => {
  const coffeeType = message.coffee_type.replace('_', ' ')
  addMessage(`${coffeeType.charAt(0).toUpperCase() + coffeeType.slice(1)} ready! ☕`, 'success')
}

const initializeWebSocket = () => {
  wsService.connect()
  wsService.on('connected', handleConnected)
  wsService.on('disconnected', handleDisconnected)
  wsService.on('status_update', handleStatusUpdate)
  wsService.on('coffee_made', handleCoffeeMade)
  wsService.on('error', handleError)
}

onMounted(() => {
  fetchStatus()
  initializeWebSocket()
})

onBeforeUnmount(() => {
  wsService.off('connected', handleConnected)
  wsService.off('disconnected', handleDisconnected)
  wsService.off('status_update', handleStatusUpdate)
  wsService.off('coffee_made', handleCoffeeMade)
  wsService.off('error', handleError)
  if (countdownInterval) {
    clearInterval(countdownInterval)
  }
})
</script>

<style scoped>
.coffee-machine-python-vue {
  position: relative;
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

.page-container {
  flex: 1;
  padding-bottom: 160px; /* Space for bottom navigation + footer */
  padding-top: var(--spacing-md);
}

.page-content {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.brewing-overlay {
  display: flex;
  align-items: center;
  justify-content: center;
}

.brewing-card {
  min-width: 320px;
  max-width: 500px;
  animation: scaleIn 0.3s ease-out;
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.brewing-particles {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.particle {
  display: inline-block;
  width: 8px;
  height: 8px;
  background-color: rgb(var(--v-theme-primary));
  border-radius: 50%;
  animation: particleFloat 1.5s ease-in-out infinite;
}

.particle:nth-child(1) {
  animation-delay: 0s;
}

.particle:nth-child(2) {
  animation-delay: 0.3s;
}

.particle:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes particleFloat {
  0%, 100% {
    transform: translateY(0) scale(1);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-10px) scale(1.2);
    opacity: 1;
  }
}

.coffee-ready-card,
.error-card {
  animation: scaleIn 0.3s ease-out;
}

.success-icon {
  font-size: 5rem;
  color: rgb(var(--v-theme-success));
  line-height: 1;
  animation: checkmarkPop 0.5s ease-out;
}

.error-icon {
  font-size: 5rem;
  line-height: 1;
  animation: checkmarkPop 0.5s ease-out;
}

@keyframes checkmarkPop {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

</style>

