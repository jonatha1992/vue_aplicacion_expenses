<template>
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Resumen de gastos -->
            <div class="bg-white p-4 rounded-lg shadow">
                <h2 class="text-xl font-semibold mb-4">Resumen</h2>
                <!-- Aquí puedes agregar estadísticas, gráficos, etc. -->
            </div>

            <!-- Últimos gastos -->
            <div class="bg-white p-4 rounded-lg shadow">
                <h2 class="text-xl font-semibold mb-4">Últimos Gastos</h2>
                <ExpenseList :expenses="recentExpenses" />
            </div>
        </div>
    </div>
</template>