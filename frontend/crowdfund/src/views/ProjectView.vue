<script setup>

</script>

<template>
  <div class="container-fluid">
    <!-- project id, name and description -->
    <div class="row">
      <div class="col-8">
        <h1>{{project.project_id}}: {{project.name}}</h1>
        <div class="row">
          <p>{{ project.description}}</p>
        </div>
      </div>
      <div class="col-4">
        <form action="http://localhost:5004/create_checkout_session/cus_PooH6AYiaXWQLE" method="post">
          <button class="btn btn-success" type="submit">Pledge</button>
        </form>
        <!-- <stripe-buy-button buy-button-id="buy_btn_1OzH1SBWraf69XnWbKO5uv6k"
          publishable-key="pk_test_51O4n0jBWraf69XnWSeezJW88o1buIhc2GF99LFdvQAgYaaw1zpXEeAla8XHQZS08uNrkh0EusMbzHoKWKt0Vb7g500NTzmDcIq">
        </stripe-buy-button> -->
      </div>
    </div>

    <!-- project details -->
    <div class="row">
      <!-- project_id, name, description, creator_id, funding_goal, deadline, creation_time, status, goal_reached -->
      <label for="details">More details</label>
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
