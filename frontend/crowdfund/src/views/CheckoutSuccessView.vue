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
            payment_intent_id: '',
        }
    },
    methods: {
        handleSuccess() {
            // makes a post req to back_project.py to get payment_intent_id
            const to_back_project_url = "http://localhost:5004/get_payment_intent_id/" + this.checkout_session_id
            // const to_back_project_url = "http://back_project:5004/get_payment_intent_id/" + this.checkout_session_id
            axios.get(to_back_project_url)
                .then(response => {
                    this.payment_intent_id = response.data
                    const to_tracker_url = "http://localhost:5001/project/" + this.project_id + "/tracker"
                    // const to_tracker_url = "http://tracker:5001/project/" + this.project_id + "/tracker"
                    const json = {
                        "pledge_amt": this.pledge_amt,
                        "backer_id": 7,
                        "payment_intent_id": this.payment_intent_id
                    }
                    axios.post(to_tracker_url, json)
                        .then(response => {
                            console.log(response.data)
                        })
                        .catch(error => {
                            console.log(error.message)
                        })
                        .finally(() => {
                            // then redirect the user back to the return_url
                            window.location.href = this.return_url
                        })

                })
                .catch(error => {
                    console.log(error.message)
                })
            // make a post req to tracker, which attaches the payment_intent_id to tracker data
            
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