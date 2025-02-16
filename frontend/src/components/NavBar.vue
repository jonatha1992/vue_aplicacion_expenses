<template>
  <nav class="p-4 bg-gray-200 flex items-center justify-between">
    <div class="text-xl font-bold">App de Gastos</div>
    <div>
      <button @click="emitOpenAuth('login')" class="mr-4 text-blue-700">Login</button>
      <button @click="emitOpenAuth('register')" class="text-green-700">Register</button>
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

<style scoped>
/* ...existing or custom styles... */
</style>
