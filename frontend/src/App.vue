<template>
  <div class="app">
    <header class="header">
      <h1>☕ Coffee Machine</h1>
      <p>Virtual Coffee Machine Simulator</p>
    </header>
    
    <main class="container">
      <CoffeeMachine />
    </main>
    
    <footer class="footer">
      <p>Built with FastAPI & Vue.js</p>
    </footer>
  </div>
</template>

<script setup>
import CoffeeMachine from './components/CoffeeMachine.vue'
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  text-align: center;
  color: white;
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.header h1 {
  font-size: 3rem;
  margin-bottom: var(--spacing-sm);
}

.header p {
  font-size: 1.25rem;
  opacity: 0.9;
}

main {
  flex: 1;
  padding-bottom: 0; /* Bottom nav handles this */
  min-height: calc(100vh - 200px); /* Account for header/footer */
}

.footer {
  text-align: center;
  color: white;
  padding: var(--spacing-lg);
  margin-top: var(--spacing-xl);
  opacity: 0.8;
}
</style>

