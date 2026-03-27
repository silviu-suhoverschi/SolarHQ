<template>
  <div>
    <label class="block text-xs text-gray-500 mb-1">{{ label }}</label>
    <select
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      class="w-full border border-gray-200 rounded-lg px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
    >
      <option value="">— None —</option>
      <option v-for="opt in options" :key="opt.entity_id" :value="opt.entity_id">
        {{ opt.friendly_name || opt.entity_id }}
      </option>
    </select>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, required: true },
  /** @type {{ entity_id: string, friendly_name?: string }[]} */
  options: { type: Array, default: () => [] },
})
defineEmits(['update:modelValue'])
</script>
