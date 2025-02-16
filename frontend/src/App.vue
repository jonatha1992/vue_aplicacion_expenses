<template>
  <div id="app" class="min-h-screen bg-gray-100">
    <NavBar @open-auth="openAuthModal" />
    <header class="bg-blue-600 text-white p-4 text-center">
      <h1 class="text-3xl font-bold">Gastos</h1>
    </header>
    <main class="p-4">
      <Home />
    </main>

    <!-- Modal for authentication -->
    <div v-if="showAuthModal" class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded relative">
        <button @click="closeAuthModal" class="absolute top-2 right-2 text-gray-500">&times;</button>
        <Login :initialTab="authType" @close="closeAuthModal" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import NavBar from "./components/NavBar.vue"
import Home from "./views/Home.vue"
import Login from "./views/Login.vue"

const showAuthModal = ref(false)
const authType = ref("login")  // "login" or "register"

const openAuthModal = (type) => {
  authType.value = type
  showAuthModal.value = true
}

const closeAuthModal = () => {
  showAuthModal.value = false
}
</script>

<script>
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