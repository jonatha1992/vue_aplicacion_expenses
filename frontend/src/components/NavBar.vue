<template>
    <nav class="bg-gradient-to-r from-blue-600 to-blue-800 fixed w-full z-50 shadow-lg">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between h-16">
                <!-- Logo/Brand -->
                <div class="flex items-center space-x-4">
                    <router-link to="/" class="flex items-center space-x-2 group">
                        <svg class="h-8 w-8 text-white group-hover:text-blue-200 transition-colors duration-200"
                            fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex flex-col">
                            <span
                                class="text-white text-xl font-bold group-hover:text-blue-200 transition-colors duration-200">
                                Expenses Traker
                            </span>
                            <span v-if="authStore.user?.username" class="text-blue-200 text-sm font-medium">
                                {{ authStore.user.username }}
                            </span>
                        </div>
                    </router-link>
                </div>

                <!-- Desktop Menu -->
                <div class="hidden md:flex items-center space-x-6">
                    <template v-if="authStore.isLoggedIn">
                        <router-link to="/dashboard"
                            class="text-blue-100 hover:text-white transition-colors duration-200 text-sm uppercase tracking-wider">
                            Dashboard
                        </router-link>
                        <router-link to="/expenses"
                            class="text-blue-100 hover:text-white transition-colors duration-200 text-sm uppercase tracking-wider">
                            Gastos
                        </router-link>
                        <button @click="handleLogout"
                            class="px-4 py-2 bg-white/10 backdrop-blur-sm text-white rounded-lg hover:bg-white/20 transition-all duration-200 text-sm uppercase tracking-wider">
                            Cerrar Sesión
                        </button>
                    </template>
                    <template v-else>
                        <button @click="$emit('open-auth', 'login')"
                            class="px-4 py-2 bg-white/10 backdrop-blur-sm text-white rounded-lg hover:bg-white/20 transition-all duration-200">
                            Iniciar Sesión
                        </button>
                        <button @click="$emit('open-auth', 'register')"
                            class="px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-blue-50 transition-all duration-200 shadow-md">
                            Registrarse
                        </button>
                    </template>
                </div>

                <!-- Mobile menu button -->
                <div class="md:hidden flex items-center">
                    <button @click="isOpen = !isOpen"
                        class="text-white p-2 rounded-lg hover:bg-white/10 transition-colors duration-200">
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path v-if="!isOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 6h16M4 12h16M4 18h16" />
                            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </div>

            <!-- Mobile Menu -->
            <div v-show="isOpen" class="md:hidden transition-all duration-300 ease-in-out"
                :class="{ 'opacity-100 translate-y-0': isOpen, 'opacity-0 -translate-y-4': !isOpen }">
                <div class="px-2 pt-2 pb-3 space-y-1 bg-white/10 backdrop-blur-sm rounded-lg mt-2">
                    <template v-if="authStore.isLoggedIn">
                        <router-link to="/dashboard"
                            class="block px-3 py-2 text-blue-100 hover:text-white hover:bg-white/10 rounded-md transition-all duration-200"
                            @click="isOpen = false">
                            Dashboard
                        </router-link>
                        <router-link to="/expenses"
                            class="block px-3 py-2 text-blue-100 hover:text-white hover:bg-white/10 rounded-md transition-all duration-200"
                            @click="isOpen = false">
                            Gastos
                        </router-link>
                        <button @click="handleLogout"
                            class="w-full text-left px-3 py-2 text-blue-100 hover:text-white hover:bg-white/10 rounded-md transition-all duration-200">
                            Cerrar Sesión
                        </button>
                    </template>
                    <template v-else>
                        <button @click="handleMobileAuth('login')"
                            class="w-full text-left px-3 py-2 text-blue-100 hover:text-white hover:bg-white/10 rounded-md transition-all duration-200">
                            Iniciar Sesión
                        </button>
                        <button @click="handleMobileAuth('register')"
                            class="w-full text-left px-3 py-2 text-blue-100 hover:text-white hover:bg-white/10 rounded-md transition-all duration-200">
                            Registrarse
                        </button>
                    </template>
                </div>
            </div>
        </div>
    </nav>
    <div class="h-16"></div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
const isOpen = ref(false)
const emit = defineEmits(['open-auth'])

const handleLogout = async () => {
    await authStore.logout()
    router.push('/')
    isOpen.value = false
}

const handleMobileAuth = (type) => {
    emit('open-auth', type)
    isOpen.value = false
}
</script>

<style scoped>
.router-link-active {
    @apply font-semibold text-white bg-white/10 rounded-md;
}

/* Animaciones suaves */
.transition-all {
    transition-property: all;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 200ms;
}
</style>