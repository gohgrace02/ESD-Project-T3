<template>
  <div class="d-flex justify-content-between align-items-center mb-4">
    <!-- <nav style="--bs-breadcrumb-divider: '>';">
      <ol class="breadcrumb m-0">
        <li v-if="is_creator" class="breadcrumb-item"><a href="/creator">Home</a></li>
        <li v-else class="breadcrumb-item"><a href="/backer">Home</a></li>
        <li class="breadcrumb-item active">Create a project</li>
      </ol>
    </nav> -->
    <div>
      <button class="btn btn-secondary d-flex justify-content-between pe-3 ps-1" @click="back()">
        <svg width="25" height="25" viewBox="0 0 1024 1024" fill="#ffffff" class="icon" version="1.1"
          xmlns="http://www.w3.org/2000/svg">
          <path
            d="M669.6 849.6c8.8 8 22.4 7.2 30.4-1.6s7.2-22.4-1.6-30.4l-309.6-280c-8-7.2-8-17.6 0-24.8l309.6-270.4c8.8-8 9.6-21.6 2.4-30.4-8-8.8-21.6-9.6-30.4-2.4L360.8 480.8c-27.2 24-28 64-0.8 88.8l309.6 280z"
            fill="" stroke="white" stroke-width="15" />
        </svg> Back
      </button>
    </div>
    <div>
      <Logout />
    </div>
  </div>

  <div class="container-fluid">
    <form @submit.prevent="check()">
      <!-- <form @submit.prevent="createProject()"> -->
      <!-- Project details form -->
      <div class="row justify-content-center my-3">
        <div class="col-md-6 col-sm-8 bg-light rounded-3 p-3">
          <h1>Create a project</h1>
          <div class="mb-3">
            <label for="project_name" class="form-label">Project name:</label>
            <input required v-model="name" type="text" class="form-control" id="project_name">
          </div>
          <div class="mb-3">
            <label for="funding_goal" class="form-label">Funding goal ($): (input a whole number)</label>
            <input required v-model="funding_goal" type="text" class="form-control" id="funding_goal" placeholder="">
          </div>
          <div class=" row mb-3">
            <div class="col">
              <label for="deadline" class="form-label">Deadline</label>
              <input required v-model="deadline" type="date" class="form-control" id="deadline" placeholder="">
            </div>
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description:</label>
            <textarea required v-model="description" class="form-control" id="description" placeholder=""
              style="min-height: 120px;" />
          </div>
          <p class="text-danger my-3">{{ errorMsg }}</p>
          <!-- things submitted project_name, funding_goal, deadline, description
          creator_id -->
          <!-- submitted to project.py, should redirect to project page -->
          <div class="mb-3 d-flex justify-content-between">
            <button @click="this.$router.go(-1)" class="btn btn-secondary">Cancel</button>
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>

        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import Logout from '@/components/Logout.vue'

export default {
  components: {
    Logout,
  },
  data() {
    return {
      name: '',
      description: '',
      user_id: JSON.parse(sessionStorage.getItem('user')).user_id,
      funding_goal: 0,
      deadline: '',
      is_creator: JSON.parse(sessionStorage.getItem('user')).is_creator,
      errorMsg: '',
    }
  },
  methods: {
    back() {
      if (this.is_creator) {
        this.$router.push({ path: `/creator`, replace: true })
      } else {
        this.$router.push({ path: `/backer`, replace: true })
      }
    },



    createProject() {
      // const url = "http://localhost:5000/project"
      const url = "http://localhost:8000/api/v1/project?apikey=admin"
      const json = {
        "name": this.name,
        "description": this.description,
        "user_id": this.user_id,
        "funding_goal": this.funding_goal,
        "deadline": this.deadline,
        "status": "Open",
      }
      axios.post(url, json)
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.log(error.message)
        })
        .finally(() => {
          this.$router.push({ path: `/creator`, replace: true })
        })
    },
    check() {
      this.errorMsg = ''
      const json = {
        "text": this.description
      }
      axios.post("http://localhost:8000/moderate?apikey=admin", json)
      // axios.post("http://localhost:5006/moderate", json)
      .then(response => {
        if (response.data == '0') {
          // console.log("yes")
          this.createProject()
        } else {
          this.errorMsg = 'NO F*CKING VULGARITIES ALLOWED'
        }
      })
      .catch(error => {
        console.log(error.message)
      })
    }
  },
  // mounted() {
  // }
}
</script>
