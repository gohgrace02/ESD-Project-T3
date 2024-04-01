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
      <Back />
    </div>
    <div>
      <Logout />
    </div>
  </div>

  <div class="container-fluid">
    <form @submit.prevent="createProject()">
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
import Back from '@/components/Back.vue'

export default {
  components: {
    Logout,
    Back
  },
  data() {
    return {
      name: '',
      description: '',
      user_id: JSON.parse(sessionStorage.getItem('user')).user_id,
      funding_goal: 0,
      deadline: '',
      is_creator: JSON.parse(sessionStorage.getItem('user')).is_creator,
    }
  },
  methods: {
    getDetails() {
      const url = "http://localhost:5000/project/" + this.project_id
      // const url = "http://project:5000/project/" + this.project_id
      axios.get(url)
        .then(response => {
          this.project = response.data.data
        })
        .catch(error => {
          console.log(error.message)
        })
    },
    createProject() {
      const url = "http://localhost:5000/project"
      // const url = "http://project:5000/project"
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
          this.$router.go(-1)
        })
    },
  },
  mounted() {
    this.getDetails()
  }
}
</script>
