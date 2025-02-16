<template>
  <div class="max-w-md mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Login</h1>
    <form @submit.prevent="handleEmailLogin" class="mb-6">
      <input v-model="email" type="email" placeholder="Email" class="border p-2 mb-2 w-full"/>
      <input v-model="password" type="password" placeholder="Contraseña" class="border p-2 mb-2 w-full"/>
      <button type="submit" class="w-full p-2 bg-blue-500 text-white rounded">Ingresar</button>
    </form>
    <button @click="handleGoogleLogin" class="w-full p-2 bg-red-500 text-white rounded mb-6">
      Ingresar con Google
    </button>
    <hr class="mb-6" />
    <h1 class="text-2xl font-bold mb-4">Registro</h1>
    <form @submit.prevent="handleEmailRegister">
      <input v-model="emailRegister" type="email" placeholder="Email" class="border p-2 mb-2 w-full"/>
      <input v-model="passwordRegister" type="password" placeholder="Contraseña" class="border p-2 mb-2 w-full"/>
      <input v-model="displayName" type="text" placeholder="Nombre" class="border p-2 mb-2 w-full"/>
      <button type="submit" class="w-full p-2 bg-green-500 text-white rounded">Registrarse</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { loginWithEmail, signInWithGoogle, registerWithEmail } from "../services/authService";

const email = ref("");
const password = ref("");

const emailRegister = ref("");
const passwordRegister = ref("");
const displayName = ref("");

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

const handleEmailRegister = async () => {
  try {
    const user = await registerWithEmail(emailRegister.value, passwordRegister.value, displayName.value);
    console.log("Usuario registrado:", user);
  } catch (e) {
    console.error("Error en registro:", e);
  }
};
</script>
