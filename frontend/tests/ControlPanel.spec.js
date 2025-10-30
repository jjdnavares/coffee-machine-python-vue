import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ControlPanel from '../src/components/ControlPanel.vue'

describe('ControlPanel', () => {
  const mockStatusWithResources = {
    water_level: 200.0,
    water_capacity: 2000.0,
    coffee_level: 200.0,
    coffee_capacity: 500.0,
    total_coffees_made: 0
  }

  it('renders all three coffee buttons', () => {
    const wrapper = mount(ControlPanel, {
      props: {
        status: mockStatusWithResources
      }
    })

    expect(wrapper.text()).toContain('Make Coffee')
    expect(wrapper.text()).toContain('Espresso')
    expect(wrapper.text()).toContain('Double Espresso')
    expect(wrapper.text()).toContain('Americano')
    
    const buttons = wrapper.findAll('button')
    expect(buttons.length).toBe(3)
  })

  it('displays correct recipe information for each coffee type', () => {
    const wrapper = mount(ControlPanel, {
      props: {
        status: mockStatusWithResources
      }
    })

    expect(wrapper.text()).toContain('8g coffee, 24ml water')
    expect(wrapper.text()).toContain('16g coffee, 48ml water')
    expect(wrapper.text()).toContain('16g coffee, 148ml water')
  })

  it('enables buttons when resources are sufficient', () => {
    const wrapper = mount(ControlPanel, {
      props: {
        status: mockStatusWithResources,
        loading: false
      }
    })

    const buttons = wrapper.findAll('button')
    // All buttons should be enabled with sufficient resources
    expect(buttons[0].attributes('disabled')).toBeUndefined()
    expect(buttons[1].attributes('disabled')).toBeUndefined()
    expect(buttons[2].attributes('disabled')).toBeUndefined()
  })

  it('disables espresso button when resources are insufficient', () => {
    const lowStatus = {
      water_level: 10.0,  // Not enough for espresso (needs 24ml)
      coffee_level: 10.0,  // Enough for espresso (needs 8g)
      water_capacity: 2000.0,
      coffee_capacity: 500.0
    }

    const wrapper = mount(ControlPanel, {
      props: {
        status: lowStatus,
        loading: false
      }
    })

    const buttons = wrapper.findAll('button')
    // Espresso button should be disabled (not enough water)
    expect(buttons[0].attributes('disabled')).toBeDefined()
  })

  it('disables double espresso button when resources are insufficient', () => {
    const lowStatus = {
      water_level: 20.0,  // Not enough for double espresso (needs 48ml)
      coffee_level: 20.0,  // Enough for double espresso (needs 16g)
      water_capacity: 2000.0,
      coffee_capacity: 500.0
    }

    const wrapper = mount(ControlPanel, {
      props: {
        status: lowStatus,
        loading: false
      }
    })

    const buttons = wrapper.findAll('button')
    // Double espresso button should be disabled
    expect(buttons[1].attributes('disabled')).toBeDefined()
  })

  it('disables americano button when resources are insufficient', () => {
    const lowStatus = {
      water_level: 100.0,  // Not enough for americano (needs 148ml)
      coffee_level: 20.0,  // Enough for americano (needs 16g)
      water_capacity: 2000.0,
      coffee_capacity: 500.0
    }

    const wrapper = mount(ControlPanel, {
      props: {
        status: lowStatus,
        loading: false
      }
    })

    const buttons = wrapper.findAll('button')
    // Americano button should be disabled (not enough water)
    expect(buttons[2].attributes('disabled')).toBeDefined()
  })

  it('disables all buttons when loading', () => {
    const wrapper = mount(ControlPanel, {
      props: {
        status: mockStatusWithResources,
        loading: true
      }
    })

    const buttons = wrapper.findAll('button')
    buttons.forEach(button => {
      expect(button.attributes('disabled')).toBeDefined()
    })
  })

  it('emits make-espresso event when espresso button is clicked', async () => {
    const wrapper = mount(ControlPanel, {
      props: {
        status: mockStatusWithResources,
        loading: false
      }
    })

    const buttons = wrapper.findAll('button')
    await buttons[0].trigger('click')

    expect(wrapper.emitted('make-espresso')).toBeTruthy()
    expect(wrapper.emitted('make-espresso')).toHaveLength(1)
  })

  it('emits make-double-espresso event when double espresso button is clicked', async () => {
    const wrapper = mount(ControlPanel, {
      props: {
        status: mockStatusWithResources,
        loading: false
      }
    })

    const buttons = wrapper.findAll('button')
    await buttons[1].trigger('click')

    expect(wrapper.emitted('make-double-espresso')).toBeTruthy()
    expect(wrapper.emitted('make-double-espresso')).toHaveLength(1)
  })

  it('emits make-americano event when americano button is clicked', async () => {
    const wrapper = mount(ControlPanel, {
      props: {
        status: mockStatusWithResources,
        loading: false
      }
    })

    const buttons = wrapper.findAll('button')
    await buttons[2].trigger('click')

    expect(wrapper.emitted('make-americano')).toBeTruthy()
    expect(wrapper.emitted('make-americano')).toHaveLength(1)
  })

  it('does not emit event when button is disabled', async () => {
    const lowStatus = {
      water_level: 10.0,
      coffee_level: 10.0,
      water_capacity: 2000.0,
      coffee_capacity: 500.0
    }

    const wrapper = mount(ControlPanel, {
      props: {
        status: lowStatus,
        loading: false
      }
    })

    const buttons = wrapper.findAll('button')
    const espressoButton = buttons[0]
    
    // Button should be disabled
    expect(espressoButton.attributes('disabled')).toBeDefined()
    
    // Try to click (should not emit)
    await espressoButton.trigger('click')
    
    // Should not emit event when disabled
    expect(wrapper.emitted('make-espresso')).toBeFalsy()
  })

  it('shows spinner when loading and currentAction matches', () => {
    const wrapper = mount(ControlPanel, {
      props: {
        status: mockStatusWithResources,
        loading: true,
        currentAction: 'espresso'
      }
    })

    // Should show spinner for espresso button
    const espressoButton = wrapper.findAll('button')[0]
    expect(espressoButton.html()).toContain('spinner')
  })

  it('handles empty status gracefully', () => {
    const wrapper = mount(ControlPanel, {
      props: {
        status: {},
        loading: false
      }
    })

    const buttons = wrapper.findAll('button')
    // All buttons should be disabled with empty status
    buttons.forEach(button => {
      expect(button.attributes('disabled')).toBeDefined()
    })
  })

  it('handles null status gracefully', () => {
    const wrapper = mount(ControlPanel, {
      props: {
        status: null,
        loading: false
      }
    })

    const buttons = wrapper.findAll('button')
    // All buttons should be disabled with null status
    buttons.forEach(button => {
      expect(button.attributes('disabled')).toBeDefined()
    })
  })
})

