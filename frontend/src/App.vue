<template>
    <NavBar @open-auth="openAuthModal" />
    <div id="app" class="min-h-screen bg-gray-100">
        <main class="p-4">
            <template v-if="authStore.isLoggedIn">
                <Home />
            </template>
            <div v-else class="text-center mt-10">
                Por favor, inicia sesión para ver tus gastos
            </div>
        </main>

        <!-- Modal for authentication -->
        <div v-if="showAuthModal && !authStore.isLoggedIn"
            class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50">
            <div class="bg-white p-6 rounded relative">
                <button @click="closeAuthModal" class="absolute top-2 right-2 text-gray-500">&times;</button>
                <Login v-if="authType === 'login'" @close="closeAuthModal" @open-auth="openAuthModal" />
                <Register v-else-if="authType === 'register'" @close="closeAuthModal" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useAuthStore } from "./stores/authStore";
import NavBar from "./components/NavBar.vue";
import Home from "./views/Home.vue";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";

const showAuthModal = ref(false);
const authType = ref("login");
const authStore = useAuthStore();

const openAuthModal = (type) => {
    authType.value = type;
    showAuthModal.value = true;
};

const closeAuthModal = () => {
    showAuthModal.value = false;
};

onMounted(() => {
    authStore.initializeAuth();
    if (!authStore.isLoggedIn) {
        openAuthModal("login");
    }
});

watch(() => authStore.isLoggedIn, (newValue) => {
    if (newValue) {
        showAuthModal.value = false;
    }
});
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