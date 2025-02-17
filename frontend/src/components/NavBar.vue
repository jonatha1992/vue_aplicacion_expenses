<template>
    <nav class="bg-blue-600 shadow-md">
        <div class="container mx-auto px-6 py-3 flex items-center justify-between">
            <h3 class="text-2xl font-semibold text-white">
                Expense Tracker
            </h3>
            <div>
                <!-- Si hay usuario, se muestra su username -->
                <span v-if="user" class="text-white mr-4">Bienvenido, {{ user.username }}</span>
                <!-- Botones de login/registro si no hay usuario -->
                <button v-else @click="$emit('open-auth', 'login')" class="px-4 py-2 bg-white text-blue-600 rounded">
                    Login
                </button>
            </div>
        </div>
    </nav>
</template>


<script setup>
import { ref } from 'vue'
const user = ref(null)
const emit = defineEmits(["open-auth"])

</script>
