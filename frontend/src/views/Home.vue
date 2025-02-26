<template>
    <div class="container mx-auto p-4">
        <div class="text-center">
            <h1 class="text-4xl font-bold mb-4">Bienvenido a Gestor de Gastos</h1>
            <p class="text-xl mb-8">Una aplicación simple para gestionar tus gastos diarios</p>

            <div v-if="authStore.isLoggedIn" class="mb-4">
                <router-link to="/expenses"
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Ir a Gestión de Gastos
                </router-link>
            </div>

            <div v-else class="mb-4">
                <!-- Cambiar router-link por button -->
                <button @click="openAuthModal('login')"
                    class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
                    Iniciar Sesión
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useAuthStore } from '../stores/authStore';
import { inject } from 'vue'; // Agregar esta importación

const authStore = useAuthStore();
const openAuthModal = inject('openAuthModal'); // Inyectar la función desde App.vue
</script>