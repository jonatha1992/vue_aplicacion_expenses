<template>
    <div class="min-h-[calc(100vh-4rem)] flex items-center justify-center">
        <div class="container mx-auto p-4">
            <div class="text-center max-w-2xl mx-auto">
                <h1 class="text-4xl font-bold mb-4 text-gray-800">Bienvenido a Gestor de Gastos</h1>
                <p class="text-xl mb-8 text-gray-600">Una aplicación simple para gestionar tus gastos diarios</p>

                <!-- Features Section -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="p-4 bg-white rounded-lg shadow-md">
                        <div class="text-blue-500 text-2xl mb-2">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <h3 class="font-semibold text-lg mb-2">Seguimiento Simple</h3>
                        <p class="text-gray-600">Registra y monitorea tus gastos de manera fácil y rápida</p>
                    </div>
                    <div class="p-4 bg-white rounded-lg shadow-md">
                        <div class="text-blue-500 text-2xl mb-2">
                            <i class="fas fa-chart-pie"></i>
                        </div>
                        <h3 class="font-semibold text-lg mb-2">Reportes Detallados</h3>
                        <p class="text-gray-600">Visualiza tus gastos con gráficos y estadísticas claras</p>
                    </div>
                    <div class="p-4 bg-white rounded-lg shadow-md">
                        <div class="text-blue-500 text-2xl mb-2">
                            <i class="fas fa-mobile-alt"></i>
                        </div>
                        <h3 class="font-semibold text-lg mb-2">Acceso en Cualquier Lugar</h3>
                        <p class="text-gray-600">Gestiona tus gastos desde cualquier dispositivo</p>
                    </div>
                </div>

                <!-- Call to Action Buttons -->
                <div class="space-y-4 md:space-y-0 md:space-x-4">
                    <div v-if="authStore.isLoggedIn" class="inline-block">
                        <router-link to="/expenses"
                            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 ease-in-out transform hover:-translate-y-1">
                            Ir a Gestión de Gastos
                        </router-link>
                    </div>
                    <div v-else class="inline-block">
                        <button @click="openAuthModal('login')"
                            class="bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 ease-in-out transform hover:-translate-y-1">
                            Iniciar Sesión
                        </button>
                        <button @click="openAuthModal('register')"
                            class="ml-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 ease-in-out transform hover:-translate-y-1">
                            Registrarse
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useAuthStore } from '../stores/authStore';
import { inject } from 'vue';

const authStore = useAuthStore();
const openAuthModal = inject('openAuthModal');
</script>

<style scoped>
.container {
    transition: all 0.3s ease;
}

@media (max-width: 768px) {
    .container {
        padding: 2rem 1rem;
    }
}
</style>