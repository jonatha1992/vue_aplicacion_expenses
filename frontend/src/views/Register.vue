<template>
    <div class="max-w-md mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Registro</h1>
        <form @submit.prevent="handleEmailRegister">
            <input v-model="emailRegister" type="email" placeholder="Email" class="border p-2 mb-2 w-full" />
            <input v-model="passwordRegister" type="password" placeholder="Contraseña" class="border p-2 mb-2 w-full" />
            <input v-model="displayName" type="text" placeholder="Nombre" class="border p-2 mb-2 w-full" />
            <button type="submit" class="w-full p-2 bg-green-500 text-white rounded">Registrarse</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { registerWithEmail } from "../services/authService";

const emailRegister = ref("");
const passwordRegister = ref("");
const displayName = ref("");

const handleEmailRegister = async () => {
    try {
        const user = await registerWithEmail(emailRegister.value, passwordRegister.value, displayName.value);
        console.log("Usuario registrado:", user);
    } catch (e) {
        console.error("Error en registro:", e);
    }
};
</script>
