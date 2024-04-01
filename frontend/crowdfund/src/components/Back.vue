<template>
    <button class="btn btn-secondary d-flex justify-content-between pe-3 ps-1" @click="back()">
        <svg width="25" height="25" viewBox="0 0 1024 1024"
            fill="#ffffff" class="icon" version="1.1" xmlns="http://www.w3.org/2000/svg">
            <path
                d="M669.6 849.6c8.8 8 22.4 7.2 30.4-1.6s7.2-22.4-1.6-30.4l-309.6-280c-8-7.2-8-17.6 0-24.8l309.6-270.4c8.8-8 9.6-21.6 2.4-30.4-8-8.8-21.6-9.6-30.4-2.4L360.8 480.8c-27.2 24-28 64-0.8 88.8l309.6 280z"
                fill="" stroke="white" stroke-width="15"/>
        </svg> Back</button>
</template>

<script>
export default {
    methods: {
        props: ['is_creator'],
        back() {
            if (this.is_creator) {
                this.$router.push({ path: `/creator`, replace: true })
            } else {
                this.$router.push({ path: `/backer`, replace: true })
            }
            // this.$router.go(-1)
        }
    }
}
</script>