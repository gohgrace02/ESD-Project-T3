<script setup>

</script>

<template>

  <div class="container-fluid">
    <form @submit.prevent="validate()">
      <!-- Project details form -->
      <div class="row justify-content-center my-3">
        <div style="width: 400px;" class="bg-light rounded-3 p-3">
          <h1 class="text-center">Sign up</h1>
          <div class="mb-3">
            <label for="email" class="form-label">Email:</label>
            <input required v-model="email" type="email" class="form-control" id="email">
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password:</label>
            <input required v-model="password" type="password" class="form-control" id="password" placeholder="">
          </div>
          <div class="mb-3">
            <label for="confirm" class="form-label">Confirm password:</label>
            <input required v-model="confirm" type="password" class="form-control" id="confirm" placeholder="">
            <p v-if="errorMsg" class="text-danger">{{ errorMsg }}</p>
          </div>
          <div class="mb-3">
            <input v-model="creator" type="checkbox" class="form-check-input" id="creator">
            <label for="creator" class="form-check-label ms-2">I am a creator!</label>
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
      confirm: '',
      creator: false,

      errorMsg: '',

    }
  },
  methods: {
    login() {
        const data = {
          email: this.email,
          password: this.password,
          creator: this.creator,
        }
        
        axios.post(url, data)
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.log(error.message)
        })
    },
    validate() {
      if (this.password !== this.confirm) {
        this.errorMsg = 'Passwords do not match'
        console.log('Passwords do not match')
      } else {
        this.errorMsg = ''
        this.login()
      }
    },

  },
  mounted() {
    
  }
}
</script>