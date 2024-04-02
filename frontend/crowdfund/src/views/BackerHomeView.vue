<template>
  <div class="row d-flex justify-content-between mb-4">
    <div class="col">
      <div class="dropdown">
        <button class="btn btn-primary dropdown-toggle" type="button" data-bs-toggle="dropdown">
          My pledges
        </button>
        <ul class="dropdown-menu p-2">
          <li v-for="project in projects_by_user_id" class="dropdown-item indiv-pledge my-2">
            {{ project.name }}
            <div class="pledge-buttons">
              <button @click="goToProject(project.project_id)" class="btn btn-primary">View</button>
              <button @click="cancelPledge(project.project_id)" class="btn btn-danger">Cancel</button>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="col text-end">
      <Logout />
    </div>
  </div>
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
  </div>
</template>

<script>
import axios from 'axios'
import Logout from '@/components/Logout.vue'

// import { RouterLink, userRouter } from 'vue-router';
export default {
  components: {
    Logout,
  },
  data() {
    return {
      projects: [],
      projects_by_user_id: [],
      trackers_by_user_id: [],
      search: '',
      user_id: JSON.parse(sessionStorage.getItem('user')).user_id,

    }
  },
  methods: {
    getProjects() {
      // const url = "http://localhost:5000/project"
      const url = "http://localhost:8000/api/v1/project?apikey=admin"
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
    },
    creatorName(user_id) {
      // axios.get("http://localhost:5010/user/" + user_id)
      axios.get("http://localhost:8000/user/" + user_id + "?apikey=admin")
        .then(response => {
          return response.data.data.name
        })
        .catch(error => {
          console.log(error.message)
        })
    },
    getMyPledges() {
      const url = "http://localhost:8000/get_project_by_user_id/" + this.user_id + "?apikey=admin"
      // const url = "http://localhost:5001/get_project_by_user_id/" + this.user_id
      axios.get(url)
        .then(response => {
          this.projects_by_user_id = response.data.project_list
          this.trackers_by_user_id = response.data.tracker_list
        })
        .catch(error => {
          console.log(error.message)
        })
    },
    cancelPledge(project_id) {
      for (let i=0; i<this.trackers_by_user_id.length; i++) {
        if (this.trackers_by_user_id[i]['project_id'] == project_id) {
          const tracker_id = this.trackers_by_user_id[i]['tracker_id']
          // const url = "http://localhost:5001/tracker/" + tracker_id
          const url = "http://localhost:8000/tracker/" + tracker_id + "?apikey=admin"
          axios.delete(url)
            .then(response => {
              this.getMyPledges()
            })
            .catch(error => {
              console.log(error.message)
            })
        }
      }
    },
  },
  // created() {
  //   this.getProjects()
  // },
  mounted() {
    this.getProjects()
    this.getMyPledges()
  },
  computed: {
    filteredList() {
      return this.projects.filter(project => {
        const searchTerm = this.search.toLowerCase()
        return project.name.toLowerCase().includes(searchTerm) || 
        project.project_id.toString().includes(searchTerm) ||
        project.user_id.toString().includes(searchTerm)
      })
    },
  },
}
</script>

<style>
.indiv-pledge {
  display: grid;
  grid-template-columns: auto auto;
  gap: 2rem;
}

.pledge-buttons {
  display: grid;
  grid-template-columns: auto auto;
  gap: 0.5rem;
  justify-content: end;
}

</style>