<template>
    <div class="container mx-auto p-4">
        <Loading :show="loading" message="Cargando gastos..." />

        <!-- Agregar el modal -->
        <ConfirmDialog :show="showConfirmDialog" title="Confirmar eliminación"
            message="¿Está seguro que desea eliminar este gasto?" confirm-text="Eliminar" cancel-text="Cancelar"
            confirm-button-class="bg-red-500 hover:bg-red-600" @confirm="confirmDelete" @cancel="cancelDelete" />
        <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
            {{ error }}
        </div>

        <div class="flex flex-col md:flex-row gap-6">
            <!-- Formulario de gastos -->
            <div class="w-full md:w-1/3">
                <ExpenseForm @add-expense="addExpense" @update-expense="updateExpense" @cancel-edit="cancelEdit"
                    :loading="loading" :expense-to-edit="currentExpense" />
            </div>

            <!-- Lista de gastos -->
            <div class="w-full md:w-2/3">
                <!-- <h2 class="text-xl font-bold mb-4">Todos los Gastos</h2> -->
                <ExpenseList v-if="!loading" :expenses="expenses" @remove-expense="removeExpense"
                    @edit-expense="editExpense" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import ExpenseForm from '../components/ExpenseForm.vue';
import ExpenseList from '../components/ExpenseList.vue';
import Loading from '../components/Loading.vue';
import ConfirmDialog from '../components/ConfirmDialog.vue';
import { expenseApi } from '../services/api';
import { useAuthStore } from '../stores/authStore';

const toast = useToast();
const authStore = useAuthStore();
const expenses = ref([]);
const loading = ref(false);
const error = ref(null);
const currentExpense = ref(null);
const showConfirmDialog = ref(false);
const expenseToDelete = ref(null);

const fetchExpenses = async () => {
    if (!authStore.isLoggedIn) return;

    loading.value = true;
    error.value = null;
    try {
        const response = await expenseApi.getAll();
        if (response.data.length === 0) {
            toast.info('No existen gastos en la base de datos');
        }
        expenses.value = response.data;
    } catch (e) {
        toast.error('Error al cargar los gastos');
        console.error(e);
    } finally {
        loading.value = false;
    }
};

const addExpense = async (expense) => {
    loading.value = true;
    error.value = null;
    try {
        const response = await expenseApi.create(expense);
        expenses.value.push(response.data);
        toast.success('Gasto agregado exitosamente');
    } catch (e) {
        toast.error('Error al agregar el gasto');
        console.error(e);
    } finally {
        loading.value = false;
    }
};

const updateExpense = async (id, updatedExpense) => {
    loading.value = true;
    error.value = null;
    try {
        const response = await expenseApi.update(id, updatedExpense);
        const index = expenses.value.findIndex(exp => exp.id === id);
        if (index !== -1) {
            expenses.value[index] = response.data;
        }
        currentExpense.value = null;
        toast.success('Gasto actualizado exitosamente');
    } catch (e) {
        toast.error('Error al actualizar el gasto');
        console.error(e);
    } finally {
        loading.value = false;
    }
};

const removeExpense = (id) => {
    expenseToDelete.value = id;
    showConfirmDialog.value = true;
};

const confirmDelete = async () => {
    loading.value = true;
    try {
        await expenseApi.delete(expenseToDelete.value);
        expenses.value = expenses.value.filter(exp => exp.id !== expenseToDelete.value);
        toast.success('Gasto eliminado exitosamente');
    } catch (e) {
        toast.error('Error al eliminar el gasto');
        console.error(e);
    } finally {
        loading.value = false;
        showConfirmDialog.value = false;
        expenseToDelete.value = null;
    }
};

const cancelDelete = () => {
    showConfirmDialog.value = false;
    expenseToDelete.value = null;
};

const editExpense = (expense) => {
    currentExpense.value = expense;
};

const cancelEdit = () => {
    currentExpense.value = null;
};

onMounted(() => {
    if (authStore.isLoggedIn) {
        fetchExpenses();
    }
});
</script>