<template>
  <div class="coffee-machine">
    <!-- Messages always visible -->
    <MessageDisplay
      :messages="messages"
      @remove-message="removeMessage"
    />
    
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
          @make-americano="makeAmericano"
        />
        <!-- Quick status summary on make coffee page -->
        <div class="quick-status">
          <div class="quick-status-item">
            <span class="quick-status-label">Water:</span>
            <span class="quick-status-value">{{ formatNumber(status?.water_level || 0) }}ml</span>
          </div>
          <div class="quick-status-item">
            <span class="quick-status-label">Coffee:</span>
            <span class="quick-status-value">{{ formatNumber(status?.coffee_level || 0) }}g</span>
          </div>
        </div>
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
import { ref, onMounted } from 'vue'
import { coffeeAPI } from '../services/api'
import { formatMessage, formatNumber } from '../utils/helpers'
import StatusDisplay from './StatusDisplay.vue'
import ControlPanel from './ControlPanel.vue'
import FillControls from './FillControls.vue'
import MessageDisplay from './MessageDisplay.vue'
import TabNavigation from './TabNavigation.vue'

// Tab management - 'make-coffee' is the default entry point
const activeTab = ref('make-coffee')

const status = ref(null)
const loading = ref(false)
const currentAction = ref('')
const messages = ref([])
let messageIdCounter = 0

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
    if (response.data.success) {
      status.value = response.data.data
    }
  } catch (error) {
    handleError(error)
  } finally {
    loading.value = false
  }
}

const makeCoffee = async (type, actionName) => {
  try {
    loading.value = true
    currentAction.value = actionName
    
    let response
    switch (type) {
      case 'espresso':
        response = await coffeeAPI.makeEspresso()
        break
      case 'double-espresso':
        response = await coffeeAPI.makeDoubleEspresso()
        break
      case 'americano':
        response = await coffeeAPI.makeAmericano()
        break
    }
    
    if (response.data.success) {
      addMessage(formatMessage(response), 'success')
      await fetchStatus()
    }
  } catch (error) {
    handleError(error)
  } finally {
    loading.value = false
    currentAction.value = ''
  }
}

const makeEspresso = () => makeCoffee('espresso', 'espresso')
const makeDoubleEspresso = () => makeCoffee('double-espresso', 'double-espresso')
const makeAmericano = () => makeCoffee('americano', 'americano')

const fillWater = async (amount) => {
  try {
    loading.value = true
    const response = await coffeeAPI.fillWater(amount)
    if (response.data.success) {
      addMessage(formatMessage(response), 'success')
      await fetchStatus()
    }
  } catch (error) {
    handleError(error)
  } finally {
    loading.value = false
  }
}

const fillCoffee = async (amount) => {
  try {
    loading.value = true
    const response = await coffeeAPI.fillCoffee(amount)
    if (response.data.success) {
      addMessage(formatMessage(response), 'success')
      await fetchStatus()
    }
  } catch (error) {
    handleError(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStatus()
})
</script>

<style scoped>
.coffee-machine {
  position: relative;
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

.page-container {
  flex: 1;
  padding-bottom: 80px; /* Space for bottom navigation */
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

.quick-status {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-md);
  margin-top: var(--spacing-lg);
  display: flex;
  justify-content: space-around;
  gap: var(--spacing-md);
}

.quick-status-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
}

.quick-status-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.quick-status-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
}
</style>

