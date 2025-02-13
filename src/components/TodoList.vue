<template>
  <div class="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
    <h1 class="text-2xl font-bold mb-4">Lista de Tareas</h1>
    
    <div class="flex mb-4">
      <input 
        v-model="newTask" 
        @keyup.enter="addTask"
        class="flex-1 p-2 border rounded-l focus:outline-none"
        placeholder="Nueva tarea..."
      />
      <button 
        @click="addTask"
        class="bg-blue-500 text-white px-4 py-2 rounded-r hover:bg-blue-600"
      >
        Agregar
      </button>
    </div>

    <ul class="space-y-2">
      <li v-for="(task, index) in tasks" :key="index" class="flex items-center justify-between p-2 border rounded">
        <span :class="{ 'line-through': task.completed }">{{ task.text }}</span>
        <div>
          <button 
            @click="toggleTask(index)"
            class="mr-2 text-sm px-2 py-1 rounded"
            :class="task.completed ? 'bg-green-500' : 'bg-gray-200'"
          >
            ✓
          </button>
          <button 
            @click="deleteTask(index)"
            class="bg-red-500 text-white text-sm px-2 py-1 rounded hover:bg-red-600"
          >
            ×
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newTask: '',
      tasks: []
    }
  },
  created() {
    const savedTasks = localStorage.getItem('tasks')
    if (savedTasks) {
      this.tasks = JSON.parse(savedTasks)
    }
  },
  methods: {
    addTask() {
      if (this.newTask.trim()) {
        this.tasks.push({
          text: this.newTask,
          completed: false
        })
        this.newTask = ''
        this.saveTasks()
      }
    },
    toggleTask(index) {
      this.tasks[index].completed = !this.tasks[index].completed
      this.saveTasks()
    },
    deleteTask(index) {
      this.tasks.splice(index, 1)
      this.saveTasks()
    },
    saveTasks() {
      localStorage.setItem('tasks', JSON.stringify(this.tasks))
    }
  }
}
</script>
