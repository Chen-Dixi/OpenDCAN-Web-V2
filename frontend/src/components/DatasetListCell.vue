<script setup>
const props = defineProps({
    dataset: Object
})

</script>
<template>
    <div class="dataset-wide-cell">
        <a href="/datasets">
            <div class="dataset-row">
                <div class="col-sm-2">
                    <!-- item image TBD: background-image css -->
                    <div class="row-item-image">
                        <img alt="Vue logo" src="../assets/header-logo.png"/>
                    </div>
                    
                </div>
                <div class="col-sm-10 row-item-title-detail">
                    <!-- title and detail -->
                    <span class="title">{{dataset.title}}</span>
                    <div class="description">
                        <p>{{dataset.description}}</p>
                    </div>
                </div>
            </div>
        </a>
    </div>
</template>
<style scoped>
.dataset-wide-cell {
    border-bottom: 1px solid #ddd;
    padding: 4px;
    min-height: 6rem;
    margin: .5rem 0;
}
.dataset-wide-cell>a{
    text-decoration: none;
}
.dataset-row {
    align-items: center;
    justify-content: center;
    display: flex;
}
.col-sm-2 {
    flex: 0 0 16.6666666667%; /* grow 0, shrink 0*/
    max-width: 16.6666666667%;
    
}
.col-sm-10 {
    flex: 0 0 83.3333333333%;
    max-width: 83.3333333333%;
}
.dataset-row .row-item-image {
    padding: 0 15px;
    margin: 0;
    /* TBD image ratio */
}
.dataset-row .row-item-title-detail {
    padding: 0 15px;
    text-align: left;
    text-decoration: none;
    position: relative;
}
.dataset-wide-cell .title{
    font-weight: 700;
    font-size: 18px;
    color: #0096b1;
    
}
.row-item-title-detail .description>p{
    overflow: hidden;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    display: -webkit-box;
    color: #212529;
    hyphens: auto;
}
</style>