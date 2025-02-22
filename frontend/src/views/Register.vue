<template>
    <div class="max-w-md mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Registro</h1>

        <!-- Add error display -->
        <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
            {{ error }}
        </div>

        <form @submit.prevent="handleEmailRegister">
            <input v-model="emailRegister" type="email" placeholder="Email" class="border p-2 mb-2 w-full" required />
            <input v-model="passwordRegister" type="password" placeholder="Contraseña" class="border p-2 mb-2 w-full"
                required />
            <input v-model="displayName" type="text" placeholder="Nombre" class="border p-2 mb-2 w-full" required />
            <button type="submit" class="w-full p-2 bg-green-500 text-white rounded hover:bg-green-600"
                :disabled="loading">
                {{ loading ? 'Registrando...' : 'Registrarse' }}
            </button>
        </form>

        <!-- Add login link -->
        <p class="mt-4 text-center">
            ¿Ya tienes una cuenta?
            <button @click="switchToLogin" class="text-blue-500 underline">Inicia sesión</button>
        </p>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { registerWithEmail } from "../services/authService";
import { useAuthStore } from "../stores/authStore";
import { useRouter } from 'vue-router';

const router = useRouter();
const authStore = useAuthStore();
const emailRegister = ref("");
const passwordRegister = ref("");
const displayName = ref("");
const error = ref(null);
const loading = ref(false);
const emit = defineEmits(['close', 'open-auth']);

const handleEmailRegister = async () => {
    loading.value = true;
    error.value = null;

    try {
        const response = await registerWithEmail(
            emailRegister.value,
            passwordRegister.value,
            displayName.value
        );

        // Store user data
        authStore.setUser(
            {
                username: displayName.value,
                email: emailRegister.value
            },
            response.access_token
        );

        emit('close');
        router.push('/home');
    } catch (e) {
        if (e.response?.data?.detail) {
            error.value = e.response.data.detail;
        } else if (e.code) {
            // Firebase errors
            const errorMessages = {
                'auth/email-already-in-use': 'El email ya está registrado',
                'auth/invalid-email': 'Email inválido',
                'auth/operation-not-allowed': 'Operación no permitida',
                'auth/weak-password': 'La contraseña es muy débil'
            };
            error.value = errorMessages[e.code] || 'Error en el registro';
        } else {
            error.value = 'Error en el registro';
        }
    } finally {
        loading.value = false;
    }
};

const switchToLogin = () => {
    emit('open-auth', 'login');
};
</script>