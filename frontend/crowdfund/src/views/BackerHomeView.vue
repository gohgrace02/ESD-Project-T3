<script setup>

</script>

<template>
  <div class="container-fluid">
    <!-- search -->
    <div class="row mb-4 p-3 bg-light rounded-5">
      <div class="mb-3">
        <label for="search" class="form-label fw-bold">Search:</label>
        <input type="text" v-model="search" class="form-control" id="search" placeholder="Start typing to search...">
      </div>
    </div>

    <!-- display results -->
    <div class="row">
      <h5 for="projects_table" class="form-label fw-bold">Projects available:</h5>
      <table class="table table-hover text-end" id="projects_table">
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
          <tr v-for="project in filteredList">
            <!-- <tr v-for="project in projects"> -->
            <th scope="row">{{ project.project_id }}</th>
            <td>{{ project.name }}</td>
            <td>{{ project.creator_id }}</td>
            <td>{{ project.funding_goal }}</td>
            <td><button @click="goToProject(project.project_id)" class="btn btn-success" type="button">View
                project</button></td>
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
      projects: [],
      search: '',
    }
  },
  methods: {
    getProjects() {
      // const url = "http://localhost:5000/project"
      const url = "http://project:5000/project"
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
  // created() {
  //   this.getProjects()
  // },
  mounted() {
    this.getProjects()
  },
  computed: {
    filteredList() {
      return this.projects.filter(project => {
        const searchTerm = this.search.toLowerCase()
        return project.name.toLowerCase().includes(searchTerm) || 
        project.project_id.toString().includes(searchTerm) ||
        project.creator_id.toLowerCase().includes(searchTerm)
      })
    }
  },
}
</script>
