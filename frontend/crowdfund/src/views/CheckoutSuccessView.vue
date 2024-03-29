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
import axios from 'axios'
export default {
    data() {
        return {
            return_url: this.$route.query.return_url,
            checkout_session_id: this.$route.query.checkout_session_id,
            project_id: this.$route.query.project_id,
            pledge_amt: this.$route.query.pledge_amt,
        }
    },
    methods: {
        handleSuccess() {
            // make a post req to tracker, which attaches the checkout_session_id
            const url = "http://localhost:5001/project/" + this.project_id + "/tracker"
            const json = {
                "pledge_amt": this.pledge_amt,
                "backer_id": 7,
                "checkout_session_id": this.checkout_session_id
            }
            axios.post(url, json)
                .then(response => {
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error.message)
                })
                .finally(() => {
                    window.location.href = this.return_url
                })
            // then redirect the user back to the return_url
        },
    },
    // computed: {
    //     return_url() {
    //         return this.$route.query.return_url
    //     }
    // },
    mounted() {
        // console.log(this.$route.query.project_id)
    }
}

</script>