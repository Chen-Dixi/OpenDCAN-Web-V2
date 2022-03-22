<template>
    <el-main>
        Play
    </el-main>
</template>

<script>
export default {
    mounted(){
    // emit
    this.$emit('didSelectTab', 'play')
  },
}
</script>