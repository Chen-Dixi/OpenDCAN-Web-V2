<script lang="ts" setup>
const props = defineProps({
  task_prop: Object
})
</script>

<template>
  TrainSection: {{task_prop.name}}
</template>

<script lang="ts">
export default {

}
</script>

<style>

</style>