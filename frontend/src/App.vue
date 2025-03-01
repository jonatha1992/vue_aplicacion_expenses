<template>
    <div id="app" class="min-h-screen bg-gray-100">
        <NavBar @open-auth="openAuthModal" />

        <Teleport to="body">
            <div v-if="showAuthModal && !authStore.isLoggedIn"
                class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50 z-50">
                <div class="bg-white p-6 rounded-lg shadow-xl relative max-w-md w-full mx-4">
                    <button @click="closeAuthModal"
                        class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 text-xl">
                        &times;
                    </button>
                    <Login v-if="authType === 'login'" @close="closeAuthModal" @open-auth="openAuthModal" />
                    <Register v-else-if="authType === 'register'" @close="closeAuthModal" @open-auth="openAuthModal" />
                </div>
            </div>
        </Teleport>

        <main class="p-4">
            <router-view v-slot="{ Component }">
                <component :is="Component" />
            </router-view>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, provide } from "vue";
import { useAuthStore } from "./stores/authStore";
import { useRouter } from "vue-router";
import NavBar from "./components/NavBar.vue";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";

const router = useRouter();
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

provide('openAuthModal', openAuthModal);

onMounted(() => {
    authStore.initializeAuth();
    if (!authStore.isLoggedIn) {
        showAuthModal.value = true;
        authType.value = "login";
    }
});

watch(() => authStore.isLoggedIn, (newValue) => {
    if (newValue) {
        showAuthModal.value = false;
        router.push('/expenses');
    }
});
</script>

<style>
/* Additional global styles can be added here */
</style>