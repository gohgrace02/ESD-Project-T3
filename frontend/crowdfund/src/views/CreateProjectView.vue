<script setup>

</script>

<template>
  <nav style="--bs-breadcrumb-divider: '>';">
    <ol class="breadcrumb">
      <li class="breadcrumb-item"><a href="/creator">Home</a></li>
      <li class="breadcrumb-item active">Create a project</li>
    </ol>
  </nav>
  <div class="container-fluid">
    <form>
      <!-- Project details form -->
      <div class="row justify-content-center my-3">
        <div class="col-md-6 col-sm-8 bg-light rounded-3 p-3">
          <h1>Create a project</h1>
          <div class="mb-3">
            <label for="project_name" class="form-label">Project name:</label>
            <input v-model="name" type="text" class="form-control" id="project_name">
          </div>
          <div class="mb-3">
            <label for="funding_goal" class="form-label">Funding goal ($): (input a whole number)</label>
            <input v-model="funding_goal" type="text" class="form-control" id="funding_goal" placeholder="">
          </div>
          <div class=" row mb-3">
            <div class="col">
              <label for="deadline" class="form-label">Deadline</label>
              <input v-model="deadline" type="date" class="form-control" id="deadline" placeholder="">
            </div>
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description:</label>
            <textarea v-model="description" class="form-control" id="description" placeholder="" style="min-height: 120px;" />
          </div>
          <!-- things submitted project_name, funding_goal, deadline, description
          creator_id -->
          <!-- submitted to project.py, should redirect to project page -->
          <button @click="createProject()" type="button" class="btn btn-primary">Submit</button>

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
      name: '',
      description: '',
      creator_id: 'Creator1',
      funding_goal: 0,
      deadline: '',
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
        "creator_id": this.creator_id,
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
