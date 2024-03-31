<script setup>

</script>

<template>

  <div class="container-fluid">
    <form @submit.prevent="authenticate()">
      <!-- Project details form -->
      <div class="row justify-content-center my-3">
        <div style="width: 400px;" class="bg-light rounded-3 p-3">
          <h1 class="text-center">Login</h1>
          <div class="mb-3">
            <label for="email" class="form-label">Email:</label>
            <input required v-model="email" type="email" class="form-control" id="email">
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password:</label>
            <input required v-model="password" type="password" class="form-control" id="password" placeholder="">
          </div>
          <div class="mb-3">
            <p class="text-danger">{{ errorMsg }}</p>
          </div>
          <div class="mb-2 mt-4 text-center">
            <button type="submit" class="btn btn-primary">Login</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'login',
  data() {
    return {
      email: '',
      password: '',
      errorMsg: '',
    }
  },
  methods: {
    authenticate() {
      this.errorMsg = ''
      const data = {
        email: this.email,
        password: this.password
      }
      axios.post("http://localhost:5010/user/auth", data)
      .then(response => {
        if (response.data.code == 401) {
          this.errorMsg = response.data.message
        }
        else if (response.data.code == 201) {
          this.errorMsg = ''
          sessionStorage.setItem('isLoggedIn', 'true')
          sessionStorage.setItem('user', JSON.stringify(response.data.data))
          this.redirect(JSON.parse(sessionStorage.getItem('user')).is_creator)
        }
      })
      .catch(error => {
        if (error.code == "ERR_BAD_REQUEST") {
          this.errorMsg = 'User not found in database'
        }
      })
    },


    redirect(is_creator) {
      if (is_creator) {
        this.$router.push({ path: `/creator`, replace: true })
      }
      else {
        this.$router.push({ path: `/backer`, replace: true })
      }
    }

  },
  mounted() {
    sessionStorage.clear()
  }
}
</script>
