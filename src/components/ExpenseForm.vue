<template>
  <div class="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
    <h2 class="text-xl font-bold mb-4">Agregar Gasto</h2>
    <form @submit.prevent="submitExpense" class="flex flex-col space-y-4">
      <input
        type="text"
        v-model="expenseName"
        placeholder="Nombre del gasto"
        required
        class="border border-gray-500 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <input
        type="number"
        v-model="expenseAmount"
        placeholder="Monto"
        required
        class="border border-gray-500 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button type="submit" class="bg-blue-500 text-white rounded p-2 hover:bg-blue-600 transition">
        Agregar Gasto
      </button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      expenseName: '',
      expenseAmount: ''
    }
  },
  methods: {
    submitExpense() {
      const expense = {
        name: this.expenseName,
        amount: parseFloat(this.expenseAmount)
      }
      this.$emit('add-expense', expense)
      this.expenseName = ''
      this.expenseAmount = ''
    }
  }
}
</script>

<style scoped>
/* ...estilos opcionales... */
</style>