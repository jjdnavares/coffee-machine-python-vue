/**
 * Utility helper functions
 */

/**
 * Format number with specified decimal places
 */
export function formatNumber(num, decimals = 2) {
  return Number(num).toFixed(decimals)
}

/**
 * Calculate percentage
 */
export function calculatePercentage(current, capacity) {
  if (capacity === 0) return 0
  return (current / capacity) * 100
}

/**
 * Get status color based on percentage
 */
export function getStatusColor(percentage) {
  if (percentage >= 50) return 'green'
  if (percentage >= 20) return 'yellow'
  return 'red'
}

/**
 * Check if can make coffee based on status and recipe
 */
export function canMakeCoffee(status, recipe) {
  if (!status || !recipe) return false
  return (
    status.water_level >= recipe.water &&
    status.coffee_level >= recipe.coffee
  )
}

/**
 * Format message from API response
 */
export function formatMessage(response) {
  if (response.data?.message) {
    return response.data.message
  }
  return 'Operation completed successfully'
}

