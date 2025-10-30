/**
 * API service for communicating with the backend.
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Preserve the original error structure so components can access error.response.data.message
    // The error handling in CoffeeMachine.vue expects error.response.data.message
    if (error.response && error.response.data) {
      // Ensure we have a message property for easier access
      if (!error.response.data.message && error.response.data.error) {
        error.response.data.message = error.response.data.error
      }
    }
    return Promise.reject(error)
  }
)

/**
 * Coffee API methods
 */
export const coffeeAPI = {
  /**
   * Make an espresso
   */
  makeEspresso: () => apiClient.post('/coffee/espresso'),

  /**
   * Make a double espresso
   */
  makeDoubleEspresso: () => apiClient.post('/coffee/double-espresso'),

  /**
   * Make an americano
   */
  makeAmericano: () => apiClient.post('/coffee/americano'),

  /**
   * Get machine status
   */
  getStatus: () => apiClient.get('/status'),

  /**
   * Fill water container
   * @param {number} amount - Amount in ml
   */
  fillWater: (amount) => apiClient.post('/fill/water', { amount }),

  /**
   * Fill coffee container
   * @param {number} amount - Amount in grams
   */
  fillCoffee: (amount) => apiClient.post('/fill/coffee', { amount }),

  /**
   * Reset machine
   */
  reset: () => apiClient.post('/reset'),
}

