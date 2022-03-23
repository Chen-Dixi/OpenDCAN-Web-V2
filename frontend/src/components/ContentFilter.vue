<script setup>
const props = defineProps({
    contents: Array
})

</script>
<template>
    <el-card shadow="nerver">
        <div class="card-header">
            <span>Filter by Task</span>
        </div>
        <div>
            <el-scrollbar height="200px">
                <!-- TBD href -->
                <a v-for="content in contents" :key="content.name" href="/datasets" class="scrollbar-item">
                    {{ content.name }}
                    <span class="badge-light">{{content.badge}}</span>
                </a>
            </el-scrollbar>
        </div>
    </el-card>
</template>
<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: "Lato";
  font-weight: 500;
  font-size: 18px;
  color: #000;
  padding: 4px;
  margin-bottom: 5px;
}
.scrollbar-item {
  display: flex;
  align-items: center;
  text-align: left;
  justify-content: space-between;
  line-height: 120%;
  padding: 6px 15px 6px 10px;
  margin: 2px;
  border-radius: 4px;
  color: #0072a3;
  font-size: 16px;
  font-family: Lato;
}
.scrollbar-item span{
    float: right;
}
.el-scrollbar a{
    text-decoration: none;
}
.badge-light {
    color: #212529;
    background-color: #f8f9fa;
    padding: .25em .4em;
    text-align: center;
    border-radius: .25rem;
    font-size: 75%;
    font-weight: 700;
}
</style>