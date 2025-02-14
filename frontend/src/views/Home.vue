<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Control de Gastos</h1>
    <ExpenseForm @add-expense="addExpense" />
    <ExpenseList 
      :expenses="expenses" 
      @remove-expense="removeExpense" 
    />
  </div>
</template>

<script>
import ExpenseForm from '../components/ExpenseForm.vue';
import ExpenseList from '../components/ExpenseList.vue';

export default {
  components: {
    ExpenseForm,
    ExpenseList
  },
  data() {
    return {
      expenses: []
    };
  },
  methods: {
    addExpense(expense) {
      this.expenses.push(expense);
    },
    removeExpense(index) {
      this.expenses.splice(index, 1);
    }
  }
}
</script>

<style scoped>
/* Estilos opcionales para la vista Home */
</style>