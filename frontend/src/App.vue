<template>

    <NavBar @open-auth="openAuthModal" />
    <div id="app" class="min-h-screen bg-gray-100">
        <main class="p-4">
            <Home />
        </main>

        <!-- Modal for authentication -->
        <div v-if="showAuthModal" class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50">
            <div class="bg-white p-6 rounded relative">
                <button @click="closeAuthModal" class="absolute top-2 right-2 text-gray-500">&times;</button>
                <Login v-if="authType === 'login'" @close="closeAuthModal" />
                <Register v-else-if="authType === 'register'" @close="closeAuthModal" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue"
import NavBar from "./components/NavBar.vue"
import Home from "./views/Home.vue"
import Login from "./views/Login.vue"
import Register from "./views/Register.vue" // added import

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