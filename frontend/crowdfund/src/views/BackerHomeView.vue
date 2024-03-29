<script setup>

</script>

<template>
  <div class="container-fluid">
    <!-- search -->
    <div class="row">
      <div class="mb-3">
        <label for="search" class="form-label">Search:</label>
        <input type="text" class="form-control" id="search" placeholder="Search by project name or ID">
      </div>
    </div>

    <!-- display results -->
    <div class="row">
      <label for="projects_table" class="form-label fw-bold">Projects:</label>
      <table class="table table-hover" id="projects_table">
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Creator</th>
            <th scope="col">Funding goal</th>
            <th scope="col">Learn more</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="project in projects">
            <th scope="row">{{ project.project_id }}</th>
            <td>{{ project.name }}</td>
            <td>{{ project.creator_id }}</td>
            <td>{{ project.funding_goal }}</td>
            <td><button @click="goToProject(project.project_id)" class="btn btn-success" type="button">View project</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
// import { RouterLink, userRouter } from 'vue-router';
export default {
  data() {
    return {
      projects: []
    }
  },
  methods: {
    getProjects() {
      const url = "http://localhost:5000/project"
      axios.get(url)
      .then(response => {
        this.projects = response.data.data.projects
      })
      .catch(error => {
        console.log(error.message)
      })
    },
    goToProject(project_id) {
      this.$router.push({ name: 'project', params: { project_id: project_id } })
    }
  },
  mounted() {
    this.getProjects()
  }
}
</script>
