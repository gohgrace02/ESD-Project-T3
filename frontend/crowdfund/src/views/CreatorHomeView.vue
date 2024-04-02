<template>
  <div class="container-fluid">
    <!-- create project button -->
    <div class="row">
      <div v-if="length != 0" class="row">
        <div class="col-10">
          <h5 for="projects_table" class="form-label fw-bold">My projects:</h5>
        </div>
        <div class="col-2 text-end">
          <Logout/>
        </div>
        <table class="mt-4 table table-hover text-end" id="projects_table">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Name</th>
              <th scope="col">Funding goal</th>
              <th scope="col">Goal reached?</th>
              <th scope="col">Details</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="project in projects.projects">
              <th scope="row">{{ project.project_id }}</th>
              <td>{{ project.name }}</td>
              <td>{{ project.user_id }}</td>
              <td>{{ project.funding_goal }}</td>
              <td><button @click="goToProject(project.project_id)" class="btn btn-success" type="button">View
                  project</button></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <h5 class="text-center text-secondary mb-4">You have no projects.</h5>
      </div>
      <button @click="createProject()" class="btn btn-success">Create a project!</button>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import Logout from '@/components/Logout.vue'
import Back from '@/components/Back.vue'

// import router from '@/router';
export default {
  components: {
    Logout,
    Back
  },
  data() {
    return {
      projects: [],
      length: 0,
      user_id: JSON.parse(sessionStorage.getItem('user')).user_id,
    }
  },
  methods: {
    getProjects() {
      // const url = "http://localhost:5000/project/user_id=" + this.user_id
      const url = "http://localhost:8000/user_id=" + this.user_id + "?apikey=admin"
      axios.get(url)
      .then(response => {
        this.projects = response.data.data
        this.length = this.projects.projects.length
        // console.log(this.length)
      })
      .catch(error => {
        console.log(error.message)
      })
    },
    createProject() {
      this.$router.push({ name: 'create', 
      // params: { project_id: project_id } 
      })
    },
    goToProject(project_id) {
      this.$router.push({ name: 'project', params: {project_id: project_id} })
    },
  },
  mounted() {
    this.getProjects()
  }
}
</script>
