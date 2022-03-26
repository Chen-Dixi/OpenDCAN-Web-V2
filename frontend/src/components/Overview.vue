<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>
<script>
export default {
  mounted() {
    this.$emit('didSelectTab', 'overview')
  },
}
</script>
<template>
<el-main>
  项目主页
</el-main>
</template>

<style scoped>
a {
  color: #42b983;
}
</style>
