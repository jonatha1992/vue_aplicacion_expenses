<template>
    <div class="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg" :class="{ 'bg-yellow-50': isEditing }">
        <h2 class="text-xl font-bold mb-4">{{ isEditing ? 'Actualizar Gasto' : 'Agregar Gasto' }}</h2>
        <form @submit.prevent="handleSubmit" class="flex flex-col space-y-4">
            <select v-model="category" required :disabled="loading"
                class="border border-gray-500 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">Seleccione categoría</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                    {{ cat.name }}
                </option>
            </select>
            <input type="text" v-model="description" placeholder="Descripción del gasto" required :disabled="loading"
                class="border border-gray-500 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <input type="number" v-model="amount" placeholder="Monto" required min="0.01" step="0.01"
                :disabled="loading" @input="validateAmount"
                class="border border-gray-500 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <div class="flex gap-2">
                <button type="submit" :disabled="loading"
                    class="flex-1 text-white rounded p-2 transition disabled:opacity-50"
                    :class="isEditing ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-blue-500 hover:bg-blue-600'">
                    {{ loading ? 'Procesando...' : (isEditing ? 'Actualizar' : 'Agregar') }}
                </button>
                <button v-if="isEditing" type="button" @click="cancelEdit"
                    class="flex-1 bg-gray-500 text-white rounded p-2 hover:bg-gray-600 transition">
                    Cancelar
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { categoryApi } from '../services/api'

const props = defineProps({
    loading: Boolean,
    expenseToEdit: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['add-expense', 'update-expense', 'cancel-edit'])
const description = ref('')
const amount = ref('')
const category = ref('')
const categories = ref([])
const isEditing = ref(false)

// Watch para cuando cambie expenseToEdit
watch(() => props.expenseToEdit, (newExpense) => {
    if (newExpense) {
        description.value = newExpense.description
        amount.value = newExpense.amount
        category.value = newExpense.category_id
        isEditing.value = true
    }
}, { immediate: true })

const loadCategories = async () => {
    try {
        const response = await categoryApi.getAll()
        categories.value = response.data
    } catch (error) {
        console.error('Error loading categories:', error)
    }
}

const validateAmount = (event) => {
    const value = parseFloat(event.target.value)
    if (value <= 0) {
        event.target.value = ''
        amount.value = ''
    }
}

const handleSubmit = () => {
    if (!category.value) {
        alert('Por favor seleccione una categoría')
        return
    }

    if (parseFloat(amount.value) <= 0) {
        alert('El monto debe ser mayor a 0')
        return
    }

    const expenseData = {
        description: description.value,
        amount: parseFloat(amount.value),
        category_id: category.value,
        date: new Date().toISOString()
    }

    if (isEditing.value) {
        emit('update-expense', props.expenseToEdit.id, expenseData)
    } else {
        emit('add-expense', expenseData)
    }
    resetForm()
}

const cancelEdit = () => {
    resetForm()
    emit('cancel-edit')
}

const resetForm = () => {
    description.value = ''
    amount.value = ''
    category.value = ''
    isEditing.value = false
}

onMounted(loadCategories)
</script>

<style scoped>
/* ...estilos opcionales... */
</style>