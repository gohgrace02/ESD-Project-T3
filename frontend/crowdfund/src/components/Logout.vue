<template>
<button class="btn btn-warning" @click="logout()" >Logout</button>
</template>

<script>
export default {
    data() {
    },
    methods: {
        logout() {
            sessionStorage.clear()
            this.$router.push({ path: `/login`, replace: true })
        }
    }
}
</script>