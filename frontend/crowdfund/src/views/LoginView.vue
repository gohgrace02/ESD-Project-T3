<script setup>

</script>

<template>

  <div class="container-fluid">
    <form>
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
          <div class="mb-2 mt-4 text-center">
            <button @click="login()" type="submit" class="btn btn-primary">Login</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      email: '',
      password: '',
      description: '',
      creator_id: 'Creator1',
      funding_goal: 0,
      deadline: '',
    }
  },
  methods: {
    login() {
      console.log(this.email, this.password)
    },
  },
  mounted() {
    
  }
}
</script>
