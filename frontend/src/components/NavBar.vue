<template>
    <nav class="bg-blue-600 shadow-md">
        <div class="container mx-auto px-6 py-3">
            <div class="flex items-center justify-between">
                <!-- Logo and Navigation Links -->
                <div class="flex items-center space-x-6">
                    <router-link to="/" class="text-2xl font-semibold text-white">
                        Expense Tracker
                    </router-link>
                    <template v-if="authStore.isLoggedIn">
                        <div class="flex space-x-4">
                            <router-link to="/dashboard" class="text-white hover:text-blue-200 transition-colors"
                                :class="{ 'font-bold': $route.path === '/dashboard' }">
                                Dashboard
                            </router-link>
                            <router-link to="/expenses" class="text-white hover:text-blue-200 transition-colors"
                                :class="{ 'font-bold': $route.path === '/expenses' }">
                                Gestionar Gastos
                            </router-link>
                        </div>
                    </template>
                </div>

                <!-- User Info and Actions -->
                <div class="flex items-center space-x-4">
                    <template v-if="authStore.user">
                        <div class="flex items-center space-x-4">
                            <span class="text-white">
                                Bienvenido, <span class="font-bold">{{ authStore.user.username }}</span>
                            </span>
                            <button @click="handleLogout"
                                class="px-4 py-2 bg-white text-blue-600 rounded hover:bg-blue-100 transition-colors">
                                Cerrar Sesión
                            </button>
                        </div>
                    </template>
                    <template v-else>
                        <div class="space-x-2">
                            <button @click="$emit('open-auth', 'login')"
                                class="px-4 py-2 bg-white text-blue-600 rounded hover:bg-blue-100 transition-colors">
                                Iniciar Sesión
                            </button>
                            <button @click="$emit('open-auth', 'register')"
                                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-400 transition-colors">
                                Registrarse
                            </button>
                        </div>
                    </template>
                </div>
            </div>
        </div>
    </nav>
</template>
<script setup>
import { useAuthStore } from '../stores/authStore';
import { useRouter } from 'vue-router';

const router = useRouter();
const authStore = useAuthStore();
const emit = defineEmits(['open-auth']);

const handleLogout = async () => {
    try {
        await authStore.logout();
        router.push('/');
    } catch (error) {
        console.error("Error during logout:", error);
    }
};
</script>

<style scoped>
.router-link-active {
    font-weight: bold;
    text-decoration: underline;
}
</style>