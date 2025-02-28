<template>
    <div v-if="show" class="fixed inset-0 z-50">
        <!-- Overlay -->
        <div class="absolute inset-0 bg-black opacity-50"></div>

        <!-- Modal -->
        <div class="relative z-50 max-w-md mx-auto mt-20 bg-white rounded-lg shadow-lg">
            <div class="p-6">
                <h3 class="text-lg font-semibold mb-4">{{ title }}</h3>
                <p class="mb-6 text-gray-600">{{ message }}</p>

                <div class="flex justify-end gap-3">
                    <button @click="$emit('cancel')"
                        class="px-4 py-2 text-gray-600 bg-gray-100 rounded hover:bg-gray-200">
                        {{ cancelText }}
                    </button>
                    <button @click="$emit('confirm')" :class="confirmButtonClass" class="px-4 py-2 text-white rounded">
                        {{ confirmText }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    show: Boolean,
    title: String,
    message: String,
    confirmText: {
        type: String,
        default: 'Confirmar'
    },
    cancelText: {
        type: String,
        default: 'Cancelar'
    },
    confirmButtonClass: {
        type: String,
        default: 'bg-yellow-500 hover:bg-yellow-600'
    }
});

defineEmits(['confirm', 'cancel']);
</script>