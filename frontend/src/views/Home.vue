<template>
    <div class="container mx-auto p-4">
        <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
            {{ error }}
        </div>

        <div class="flex flex-row gap-4">
            <!-- Columna izquierda - Formulario -->
            <div class="w-1/3">
                <ExpenseForm @add-expense="addExpense" @update-expense="updateExpense" @cancel-edit="cancelEdit"
                    :loading="loading" :expense-to-edit="currentExpense" />
            </div>

            <!-- Columna derecha - Listado -->
            <div class="w-2/3">
                <div v-if="loading" class="text-center py-4">
                    Cargando...
                </div>
                <ExpenseList v-else :expenses="expenses" @remove-expense="removeExpense" @edit-expense="editExpense" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { expenseApi } from '../services/api'
import { useAuthStore } from '../stores/authStore'
import ExpenseForm from '../components/ExpenseForm.vue'
import ExpenseList from '../components/ExpenseList.vue'

const authStore = useAuthStore()
const expenses = ref([])
const loading = ref(false)
const error = ref(null)
const currentExpense = ref(null)


const fetchExpenses = async () => {
    if (!authStore.isLoggedIn) return;

    loading.value = true
    error.value = null
    try {
        const response = await expenseApi.getAll()
        if (response.data.length === 0) {
            error.value = 'No existen gastos en la base de datos'
        }
        expenses.value = response.data
    } catch (e) {
        error.value = 'Error al cargar los gastos'
        console.error(e)
    } finally {
        loading.value = false
    }
}

const addExpense = async (expense) => {
    loading.value = true
    error.value = null
    try {
        const response = await expenseApi.create(expense)
        expenses.value.push(response.data)
    } catch (e) {
        error.value = 'Error al agregar el gasto'
        console.error(e)
    } finally {
        loading.value = false
    }
}

const removeExpense = async (id) => {
    loading.value = true
    error.value = null
    try {
        console.log('Removing expense with id:', id)
        await expenseApi.delete(id)
        expenses.value = expenses.value.filter(exp => exp.id !== id)
    } catch (e) {
        error.value = 'Error al eliminar el gasto'
        console.error(e)
    } finally {
        loading.value = false
    }
}

const editExpense = (expense) => {
    currentExpense.value = expense
}

const updateExpense = async (id, updatedExpense) => {
    loading.value = true
    error.value = null
    try {
        const response = await expenseApi.update(id, updatedExpense)
        const index = expenses.value.findIndex(exp => exp.id === id)
        if (index !== -1) {
            expenses.value[index] = response.data
        }
        currentExpense.value = null
    } catch (e) {
        error.value = 'Error al actualizar el gasto'
        console.error(e)
    } finally {
        loading.value = false
    }
}

const cancelEdit = () => {
    currentExpense.value = null
}

onMounted(() => {
    if (authStore.isLoggedIn) {
        fetchExpenses()
    }
})
</script>
