<template>
    <nav class="bg-blue-600 shadow-md">
        <div class="container mx-auto px-6 py-3 flex items-center justify-between">
            <h3 class="text-2xl font-semibold text-white hover:text-blue-100 transition duration-300">
                App de Gastos
            </h3>
            <div class="space-x-4">
                <button @click="emitOpenAuth('login')"
                    class="px-4 py-2 text-blue-600 bg-white rounded-lg font-medium hover:bg-blue-50 transition duration-300">
                    Login
                </button>
                <button @click="emitOpenAuth('register')"
                    class="px-4 py-2 text-white bg-green-500 rounded-lg font-medium hover:bg-green-600 transition duration-300">
                    Register
                </button>
            </div>
        </div>
    </nav>
</template>

<script setup>
const emit = defineEmits(["open-auth"])
// Emits a custom event with the type of auth form to open.
const emitOpenAuth = (authType) => {
    emit("open-auth", authType)
}
</script>
