<template>
    <div class="max-w-md mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Login</h1>
        <form @submit.prevent="handleEmailLogin" class="mb-6">
            <input v-model="email" type="email" placeholder="Email" class="border p-2 mb-2 w-full" />
            <input v-model="password" type="password" placeholder="Contraseña" class="border p-2 mb-2 w-full" />
            <button type="submit" class="w-full p-2 bg-blue-500 text-white rounded">Ingresar</button>
        </form>
        <button @click="handleGoogleLogin"
            class="w-full p-2 bg-red-500 text-white rounded mb-6 flex items-center justify-center">
            <i class="fab fa-google mr-2"></i> Ingresar con Google
        </button>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { loginWithEmail, signInWithGoogle } from "../services/authService";

const email = ref("");
const password = ref("");

const handleEmailLogin = async () => {
    try {
        const user = await loginWithEmail(email.value, password.value);
        console.log("Usuario logeado:", user);
    } catch (e) {
        console.error("Error en login:", e);
    }
};

const handleGoogleLogin = async () => {
    try {
        const user = await signInWithGoogle();
        console.log("Usuario de Google:", user);
    } catch (e) {
        console.error("Error en Google login:", e);
    }
};
</script>
