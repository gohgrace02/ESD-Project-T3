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
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addPledgeOptionModal">+ Add pledge
          option</button>
      </div>
      <!-- modal -->
      <div class="modal fade" id="addPledgeOptionModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="title">Add pledge option</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <!-- pledge option form -->
            <!-- <form :action="`${add_pledge_option_url}`" method="post"> -->
            <form>
              <div class="modal-body">
                <div class="row justify-content-center my-3">
                  <div class="col mx-3">
                    <div class="mb-3">
                      <label for="title" class="form-label">Title:</label>
                      <input required v-model="title" type="text" class="form-control" id="title"
                        placeholder="e.g. Gold tier">
                    </div>
                    <div class="mb-3">
                      <label for="pledge_amt" class="form-label">Pledge amount ($): (input a whole number)</label>
                      <input required v-model="pledge_amt" type="number" class="form-control" id="pledge_amt"
                        placeholder="">
                    </div>
                    <div class="mb-3">
                      <label for="description" class="form-label">Description:</label>
                      <textarea required v-model="description" class="form-control" id="description"
                        style="min-height: 120px;" placeholder="What's in it for the backer?" />
                    </div>

                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <!-- things submitted: `title`, `description`, `creator_id`, `project_id`, `pledge_amt` -->
                <!-- submitted to pledge_options.py, and refreshes the page -->
                <a @click="addPledgeOption()"
                  class="btn btn-primary">Submit</a>
              </div>
            </form>
          </div>
        </div>
      </div>


    </div>
    <div class="row" id="pledge_options">
      <!-- card for each pledge option -->
      <div v-for="option in options.options" class="col-sm-6 col-md-4 mb-3">
        <div class="card">
          <div class="card-body text-center">
            <h5 class="card-title">{{ option.title }}</h5>
            <p class="card-text">{{ option.description }}</p>
            <a v-if="creator_id" @click="removeOption(option.price_id)" href="#" class="btn btn-danger">Remove
              option</a>
            <a v-else href="#" class="btn btn-success">Pledge ${{ option.pledge_amt }}</a>
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
      product_id: '',
      options: [],
      creator_id: 'Creator1',

      title: '',
      description: '',
      pledge_amt: 0,
    }
  },
  methods: {
    getDetails() {
      const url = "http://localhost:5000/project/" + this.project_id
      axios.get(url)
        .then(response => {
          this.project = response.data.data
          this.product_id = this.project.product_id
        })
        .catch(error => {
          console.log(error.message)
        })
    },
    getOptions() {
      const url = "http://localhost:5009/options/" + this.project_id
      axios.get(url)
        .then(response => {
          this.options = response.data.data
          // console.log(this.options)
        })
        .catch(error => {
          console.log(error.message)
        })
    },
    // toDollars(cents) {
    //   return cents / 100
    // },
    // toCents(dollars) {
    //   return dollars * 100
    // },
    addPledgeOption() {
      // data submitted to pledge_options.py
      // `title`, `description`, `creator_id`, `project_id`, `pledge_amt`
      const json = {
        "title": this.title,
        "description": this.description,
        "creator_id": this.creator_id,
        "project_id": this.project_id,
        "product_id": this.product_id,
        "pledge_amt": this.pledge_amt
      }
      const url = "http://localhost:5009/options/" + this.$route.params.project_id + "/add"
      axios.post(url, json)
        .then(response => {
          // data = response.data.data
          // console.log(data)
        })
        .catch(error => {
          console.log(error.message)
      })
        .finally(() => {
          this.$router.go(0)
        })
    },
    removeOption(price_id) {
      const url = "http://localhost:5009/options/" + price_id
      axios.post(url)
        .then(response => {
          // const data = response.data.data
          // console.log(data)
        })
        .catch(error => {
          console.log(error.message)
        })
        .finally(() => {
          this.$router.go(0)
        })
    }
  },
  // computed: {
  //   addPledgeOptionURL() {
  //     var url = "http://localhost:5009/options/" + this.project_id + "/add"
  //     return url
  //   },
  // },
  mounted() {
    this.getDetails()
    this.getOptions()
  }
}
</script>