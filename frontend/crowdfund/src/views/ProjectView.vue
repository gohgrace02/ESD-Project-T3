<script setup>

</script>

<template>
  <div class="container-fluid">
    <!-- project id, name and description -->
    <div class="row">
      <h1>{{project.project_id}}: {{project.name}}</h1>
      <div class="row">
        <p>{{ project.description}}</p>
      </div>
    </div>

    <!-- project details -->
    <div class="row">
      <!-- project_id, name, description, creator_id, funding_goal, deadline, creation_time, status, goal_reached -->
      <label for="details" class="fw-bold">More details</label>
      <table class="table table-hover" id="details">
        <thead>
          <tr>
            <th scope="col">Creator</th>
            <th scope="col">Funding goal</th>
            <th scope="col">Goal reached?</th>
            <th scope="col">Deadline</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">{{ project.creator_id }}</th>
            <td>{{ project.funding_goal }}</td>
            <td>{{ project.goal_reached }}</td>
            <td>{{ project.deadline }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- pledge options -->
    <div class="row mb-3">
      <div class="col">
        <label for="pledge_options" class="fw-bold" style="vertical-align: middle;">Pledge options</label>
      </div>
      <div v-if="creator_id" class="col text-end">
        <button class="btn btn-primary">+ Add pledge option</button>
      </div>

    </div>
    <div class="row" id="pledge_options">
      <!-- card for each pledge option -->
      <div v-for="option in options" class="col-sm-6 col-md-4 mb-3">
        <div class="card">
          <div class="card-body text-center">
            <h5 class="card-title">Option title</h5>
            <p class="card-text">Option description</p>
            <a href="#" class="btn btn-success">Pledge $xx.xx</a>
          </div>
        </div>
      </div>
    </div>
    <!-- <div class="col-4">
      <form class="row" action="http://localhost:5004/create_checkout_session/cus_PooH6AYiaXWQLE" method="post">
        <input type="number" class="form-control mb-3" name="pledge_amt" id="pledge_amt"
          placeholder="Enter pledge amount">
        <button class="btn btn-success" type="submit">Pledge</button>
      </form>
    </div> -->
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      project_id: this.$route.params.project_id,
      project: {},
      options: [1],
      creator_id: 'Creator1'
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