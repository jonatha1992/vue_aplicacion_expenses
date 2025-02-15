<template>
  <div class="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
    <h2 class="text-xl font-bold mb-4">Agregar Gasto</h2>
    <form @submit.prevent="submitExpense" class="flex flex-col space-y-4">
      <input
        type="text"
        v-model="description"
        placeholder="Descripción del gasto"
        required
        :disabled="loading"
        class="border border-gray-500 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <input
        type="number"
        v-model="amount"
        placeholder="Monto"
        required
        :disabled="loading"
        class="border border-gray-500 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <select
        v-model="category"
        required
        :disabled="loading"
        class="border border-gray-500 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Seleccione categoría</option>
        <option 
          v-for="cat in categories" 
          :key="cat.id" 
          :value="cat.id"
        >
          {{ cat.name }}
        </option>
      </select>
      <button 
        type="submit" 
        :disabled="loading"
        class="bg-blue-500 text-white rounded p-2 hover:bg-blue-600 transition disabled:bg-blue-300"
      >
        {{ loading ? 'Agregando...' : 'Agregar Gasto' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { categoryApi } from '../services/api'

const props = defineProps({
  loading: Boolean
})

const emit = defineEmits(['add-expense'])
const description = ref('')
const amount = ref('')
const category = ref('')
const categories = ref([])

const loadCategories = async () => {
  try {
    const response = await categoryApi.getAll()
    categories.value = response.data
  } catch (error) {
    console.error('Error loading categories:', error)
  }
}

const submitExpense = () => {
  const expense = {
    description: description.value,
    amount: parseFloat(amount.value),
    category_id: category.value,  // Cambiado para usar directamente el ID
    date: new Date().toISOString()
  }
  emit('add-expense', expense)
  description.value = ''
  amount.value = ''
  category.value = ''
}

onMounted(loadCategories)
</script>

<style scoped>
/* ...estilos opcionales... */
</style>