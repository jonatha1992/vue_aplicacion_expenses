<template>
    <nav class="bg-blue-600 shadow-md">
        <div class="container mx-auto px-6 py-3 flex items-center justify-between">
            <h3 class="text-2xl font-semibold text-white">
                Expense Tracker
            </h3>
            <div>
                <template v-if="authStore.user">
                    <span class="text-white mr-4">Bienvenido, {{ authStore.user.username }}</span>
                    <button @click="handleLogout" class="px-4 py-2 bg-white text-blue-600 rounded">
                        Logout
                    </button>
                </template>
                <button v-else @click="$emit('open-auth', 'login')" class="px-4 py-2 bg-white text-blue-600 rounded">
                    Login
                </button>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/authStore';

const authStore = useAuthStore();
const emit = defineEmits(["open-auth"]);

const handleLogout = () => {
    authStore.logout();
}
</script>
