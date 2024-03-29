<script setup>

</script>

<template>
  <div class="container-fluid">
    <form action="http://localhost:5000/project" method="post">
      <!-- Project details form -->
      <div class="row justify-content-center my-3">
        <div class="col-md-6 col-sm-8 bg-light rounded-3 p-3">
          <h1>Create a project</h1>
          <div class="mb-3">
            <label for="project_name" class="form-label">Project name:</label>
            <input type="text" class="form-control" id="project_name">
          </div>
          <div class="mb-3">
            <label for="funding_goal" class="form-label">Funding goal ($): (input a whole number)</label>
            <input type="text" class="form-control" id="funding_goal" placeholder="">
          </div>
          <div class=" row mb-3">
            <div class="col">
              <label for="deadline" class="form-label">Deadline</label>
              <input type="date" class="form-control" id="deadline" placeholder="">
            </div>
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description:</label>
            <textarea class="form-control" id="description" placeholder="" style="min-height: 120px;"/>
          </div>
          <!-- things submitted project_name, funding_goal, deadline, description
          creator_id -->
          <!-- submitted to project.py, should redirect to project page -->
          <button type="submit" class="btn btn-primary">Submit</button>

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
      project_id: this.$route.params.project_id,
      project: {}
    }
  },
  methods: {
    getDetails() {
      var url = "http://localhost:5000/project/" + this.project_id
      axios.get(url)
        .then(response => {
          this.project = response.data.data
        })
        .catch(error => {
          console.log(error.message)
        })
    },
  },
  mounted() {
    this.getDetails()
  }
}
</script>
