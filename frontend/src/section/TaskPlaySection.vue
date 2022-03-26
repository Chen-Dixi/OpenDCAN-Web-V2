<template>
    PlaySection
</template>

<script>
export default {
    mounted(){
    // emit
    this.$emit('didSelectTab', 'play')
  },
}
</script>