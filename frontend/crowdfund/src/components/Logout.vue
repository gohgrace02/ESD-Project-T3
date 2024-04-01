<template>
<button class="btn btn-warning" @click="logout()" >Logout</button>
</template>

<script>
export default {
    methods: {
        logout() {
            sessionStorage.clear()
            this.$router.push({ path: `/login`, replace: true })
        }
    }
}
</script>