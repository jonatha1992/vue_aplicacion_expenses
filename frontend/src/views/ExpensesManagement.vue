<template>
    <div class="container mx-auto p-4">
        <div class="flex flex-col md:flex-row gap-6">
            <!-- Formulario de gastos -->
            <div class="w-full md:w-1/3">
                <ExpenseForm @add-expense="addExpense" @update-expense="updateExpense" @cancel-edit="cancelEdit"
                    :loading="loading" :expense-to-edit="currentExpense" />
            </div>

            <!-- Lista de gastos -->
            <div class="w-full md:w-2/3">
                <h2 class="text-xl font-bold mb-4">Todos los Gastos</h2>
                <ExpenseList :expenses="expenses" @remove-expense="removeExpense" @edit-expense="editExpense" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import ExpenseForm from '../components/ExpenseForm.vue';
import ExpenseList from '../components/ExpenseList.vue';

const expenses = ref([]);
const loading = ref(false);
const currentExpense = ref(null);

const addExpense = (expense) => {
    expenses.value.push(expense);
};

const updateExpense = (updatedExpense) => {
    const index = expenses.value.findIndex(e => e.id === updatedExpense.id);
    if (index !== -1) {
        expenses.value[index] = updatedExpense;
    }
};

const removeExpense = (expenseId) => {
    expenses.value = expenses.value.filter(e => e.id !== expenseId);
};

const editExpense = (expense) => {
    currentExpense.value = expense;
};

const cancelEdit = () => {
    currentExpense.value = null;
};
</script>