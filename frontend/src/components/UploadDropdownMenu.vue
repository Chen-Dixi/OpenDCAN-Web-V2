<template>
    <div class="padding-15">
        <!-- <div class="cell-wrapper">
            <div class="cell-row">
                <div class="col-sm-2 cell-image">

                    <div class="background-image" style="background-image: url('/src/assets/header-logo.png')"></div>
                </div>
                <div class="col-sm-10">
                    <a class="cell-title">Images</a>
                    <div>
                        <a class="cell-description">Import images from your computer.</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="cell-wrapper">
            <div class="cell-row">
                <div class="col-sm-2 cell-image">
                    <div class="background-image" style="background-image: url('/src/assets/upload-camera.png')"></div>
                </div>
                <div class="col-sm-10">
                    <a class="cell-title">Camera</a>
                    <div>
                        <a class="cell-description">Capture Images with your webcam.</a>
                    </div>
                </div>
            </div>
        </div> -->
        <div class="cell-wrapper" @click="this.$emit('command', 'dataset')">
            <div class="cell-row">
                <div class="col-sm-2 cell-image">
                    <img src="/src/assets/upload-dataset.png" height="100%">
                </div>
                <div class="col-sm-10">
                    <a class="cell-title">Dataset</a>
                    <div>
                        <a class="cell-description">Import a structured folder of images. File must ends with one of [.zip .tar.gz, .tar]</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.cell-wrapper {
    border-bottom: 1px;
    padding: 4px;
    /* min-height: 6rem; */
    margin: .4rem 0;
    width: 280px;
}
.cell-row {
    align-items: center;
    justify-content: center;
    display: flex;
}
.cell-image{
    height: 40px;
    width: 40px;
    width: 100%;
    padding: 0 15px;
    margin: 0;
}
.cell-title{
    font-weight: 700;
    font-size: 18px;
    color: #333;
    margin-bottom: 2em;
}
.cell-description{
    color: #595c5f;
    font-weight: 200;
}
</style>
