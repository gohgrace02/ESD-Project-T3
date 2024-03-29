<template>
    <div class="container-fluid text-center">
        <div class="row justify-content-center mt-3">
            <h2 class="fw-light">Thank you for backing our project! 🎉</h2>
            <dotlottie-player src="https://lottie.host/28286376-f631-4dd4-81a9-7afd8479c541/A5rOjiUPEH.json"
                background="transparent" speed="1" style="width: 300px; height: 300px;" autoplay></dotlottie-player>
        </div>
        <button @click="handleSuccess()" class="btn btn-primary mt-3">Go back to project page</button>
    </div>
</template>

<script>
export default {
    data() {
        return {

        }
    },
    methods: {
        handleSuccess() {

        },
    }
}

</script>