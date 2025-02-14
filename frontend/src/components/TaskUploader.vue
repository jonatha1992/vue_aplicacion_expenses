<template>
  <div class="bg-white shadow rounded p-4">
    <form @submit.prevent="submitTask" class="flex flex-col space-y-4">
      <input
        type="text"
        v-model="task"
        placeholder="Ingrese una tarea"
        required
        class="border border-gray-500 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button type="submit" class="bg-blue-500 text-white rounded p-2 hover:bg-blue-600 transition">
        Subir Tarea
      </button>
    </form>
    <!-- Opcional: Listado simple de tareas subidas -->
    <ul class="mt-4 space-y-2">
      <li v-for="(t, index) in tasks" :key="index" class="p-2 border-b border-blue-200">
        {{ t }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      task: '',
      tasks: []
    }
  },
  mounted() {
    // Cargar tareas guardadas desde localStorage
    const savedTasks = localStorage.getItem('tasks')
    if (savedTasks) {
      this.tasks = JSON.parse(savedTasks)
    }
  },
  methods: {
    submitTask() {
      // Guardar la tarea en la lista y en localStorage
      this.tasks.push(this.task)
      localStorage.setItem('tasks', JSON.stringify(this.tasks))
      this.task = ''
    }
  }
}
</script>

<style scoped>
/* ...estilos opcionales... */
</style>
