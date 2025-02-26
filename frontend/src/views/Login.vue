<template>
    <div class="max-w-md mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Login</h1>

        <!-- Error Alert -->
        <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
            {{ error }}
        </div>

        <form @submit.prevent="handleEmailLogin" class="mb-6">
            <input v-model="email" type="email" placeholder="Email" class="border p-2 mb-2 w-full" required />
            <input v-model="password" type="password" placeholder="Contraseña" class="border p-2 mb-2 w-full"
                required />
            <button type="submit" class="w-full p-2 bg-blue-500 text-white rounded" :disabled="loading">
                {{ loading ? 'Ingresando...' : 'Ingresar' }}
            </button>
        </form>

        <button @click="handleGoogleLogin"
            class="w-full p-2 bg-red-500 text-white rounded mb-6 flex items-center justify-center" :disabled="loading">
            <i class="fab fa-google mr-2"></i>
            {{ loading ? 'Conectando...' : 'Ingresar con Google' }}
        </button>

        <p class="mt-4 text-center">
            ¿No tienes una cuenta?
            <button @click="switchToRegister" class="text-blue-500 underline">Regístrate</button>
        </p>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { loginWithEmail, signInWithGoogle } from "../services/authService";  // Importar de authService
import { useAuthStore } from "../stores/authStore";
import { useRouter } from 'vue-router';

const router = useRouter();
const authStore = useAuthStore();
const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const emit = defineEmits(['close', 'open-auth']);

const handleEmailLogin = async () => {
    loading.value = true;
    error.value = "";

    try {
        const response = await loginWithEmail(email.value, password.value);
        if (response.access_token) {
            authStore.setUser(response.user, response.access_token);
            emit('close');
            router.push('/expenses'); // Agregar esta línea

        } else {
            throw new Error('No se recibió token de acceso');
        }
    } catch (e) {
        error.value = e.response?.data?.detail || 'Error en login';
        console.error('Error completo:', e);
    } finally {
        loading.value = false;
    }
};

const handleGoogleLogin = async () => {
    loading.value = true;
    error.value = "";

    try {
        const response = await signInWithGoogle();  // Usar la función importada de authService
        if (response.access_token) {
            authStore.setUser(response.user, response.access_token);
            emit('close');
            router.push('/expenses'); // Agregar esta línea

        } else {
            throw new Error('No se recibió token de acceso');
        }
    } catch (e) {
        error.value = "Error al iniciar sesión con Google";
        console.error('Error completo:', e);
    } finally {
        loading.value = false;
    }
};

const switchToRegister = () => {
    emit('open-auth', 'register');
};
</script>