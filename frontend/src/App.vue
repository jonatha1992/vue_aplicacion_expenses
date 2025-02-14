<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-blue-600 text-white p-4 text-center">
      <h1 class="text-3xl font-bold">Control de Gastos</h1>
    </header>
    <main class="p-4">
      <Home />
    </main>
  </div>
</template>

<script>
import Home from './views/Home.vue'

export default {
  name: 'App',
  components: {
    Home
  }
}
</script>

<style>
/* Additional global styles can be added here */
</style>