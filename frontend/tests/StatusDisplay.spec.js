import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import StatusDisplay from '../src/components/StatusDisplay.vue'

describe('StatusDisplay', () => {
  const mockStatus = {
    water_level: 1500.0,
    water_capacity: 2000.0,
    water_percentage: 75.0,
    coffee_level: 300.0,
    coffee_capacity: 500.0,
    coffee_percentage: 60.0,
    total_coffees_made: 25
  }

  it('renders the component with status', () => {
    const wrapper = mount(StatusDisplay, {
      props: {
        status: mockStatus
      }
    })

    expect(wrapper.text()).toContain('Machine Status')
    expect(wrapper.text()).toContain('Water')
    expect(wrapper.text()).toContain('Coffee')
    expect(wrapper.text()).toContain('1500.00ml / 2000.00ml')
    expect(wrapper.text()).toContain('300.00g / 500.00g')
    expect(wrapper.text()).toContain('Total Coffees Made: 25')
  })

  it('displays water level percentage correctly', () => {
    const wrapper = mount(StatusDisplay, {
      props: {
        status: mockStatus
      }
    })

    const waterProgress = wrapper.find('.progress-fill')
    expect(waterProgress.exists()).toBe(true)
    expect(waterProgress.attributes('style')).toContain('width: 75%')
  })

  it('displays coffee level percentage correctly', () => {
    const wrapper = mount(StatusDisplay, {
      props: {
        status: mockStatus
      }
    })

    const progressBars = wrapper.findAll('.progress-fill')
    const coffeeProgress = progressBars[1]
    expect(coffeeProgress.attributes('style')).toContain('width: 60%')
  })

  it('shows correct status color class for water', () => {
    const wrapper = mount(StatusDisplay, {
      props: {
        status: mockStatus
      }
    })

    const progressBars = wrapper.findAll('.progress-fill')
    const waterProgress = progressBars[0]
    // 75% should be green (>= 50)
    expect(waterProgress.classes()).toContain('green')
  })

  it('shows yellow status color for low percentage', () => {
    const lowStatus = {
      ...mockStatus,
      water_percentage: 30.0,
      coffee_percentage: 25.0
    }

    const wrapper = mount(StatusDisplay, {
      props: {
        status: lowStatus
      }
    })

    const progressBars = wrapper.findAll('.progress-fill')
    const waterProgress = progressBars[0]
    // 30% should be yellow (>= 20 and < 50)
    expect(waterProgress.classes()).toContain('yellow')
  })

  it('shows red status color for very low percentage', () => {
    const veryLowStatus = {
      ...mockStatus,
      water_percentage: 10.0,
      coffee_percentage: 15.0
    }

    const wrapper = mount(StatusDisplay, {
      props: {
        status: veryLowStatus
      }
    })

    const progressBars = wrapper.findAll('.progress-fill')
    const waterProgress = progressBars[0]
    // 10% should be red (< 20)
    expect(waterProgress.classes()).toContain('red')
  })

  it('emits refresh-status event when refresh button is clicked', async () => {
    const wrapper = mount(StatusDisplay, {
      props: {
        status: mockStatus
      }
    })

    const refreshButton = wrapper.find('button')
    await refreshButton.trigger('click')

    expect(wrapper.emitted('refresh-status')).toBeTruthy()
    expect(wrapper.emitted('refresh-status')).toHaveLength(1)
  })

  it('handles empty status gracefully', () => {
    const wrapper = mount(StatusDisplay, {
      props: {
        status: {}
      }
    })

    expect(wrapper.text()).toContain('Machine Status')
    expect(wrapper.text()).toContain('0.00ml / 0.00ml')
    expect(wrapper.text()).toContain('Total Coffees Made: 0')
  })

  it('handles null/undefined status gracefully', () => {
    const wrapper = mount(StatusDisplay, {
      props: {
        status: null
      }
    })

    expect(wrapper.text()).toContain('Machine Status')
    // Should use default values (0) when status is null
    expect(wrapper.text()).toContain('Total Coffees Made: 0')
  })
})

