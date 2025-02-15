<template>
  <div class="mt-4">
    <h2 class="text-xl font-bold mb-2">Lista de Gastos</h2>
    <ul class="space-y-2">
      <li v-for="(expense, index) in expenses" :key="index" class="flex items-center justify-between p-2 border rounded bg-white shadow">
        <span>{{ expense.description }} - ${{ expense.amount }}</span>
        <div>
          <button 
            @click="editExpense(index)"
            class="mr-2 text-sm px-2 py-1 rounded bg-yellow-500 text-white hover:bg-yellow-600"
          >
            Editar
          </button>
          <button 
            @click="deleteExpense(index)"
            class="bg-red-500 text-white text-sm px-2 py-1 rounded hover:bg-red-600"
          >
            Eliminar
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
const props = defineProps({
  expenses: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['remove-expense', 'edit-expense'])

const deleteExpense = (index) => {
  emit('remove-expense', index)
}

const editExpense = (index) => {
  emit('edit-expense', index)
}
</script>

<style scoped>
/* ...estilos opcionales... */
</style>