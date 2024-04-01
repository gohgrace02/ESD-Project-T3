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
      <Back :is_creator="is_creator" />
    </div>
    <div>
      <Logout />
    </div>
  </div>
  <div class="container-fluid">
    <!-- project id, name and description -->
    <div class="row">
      <p class="text-secondary mb-0">[ID: {{ project.project_id}}]</p>
      <h1>{{project.name}}</h1>
      <div class="row">
        <p>{{ project.description}}</p>
      </div>
    </div>

    <!-- project details -->
    <div class="row">
      <!-- project_id, name, description, user_id, funding_goal, deadline, creation_time, status, goal_reached -->
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
            <!-- change to creator name -->
            <th scope="row">{{ project.user_id }}</th>
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
      <div v-if="is_creator" class="col text-end">
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
                <!-- things submitted: `title`, `description`, `user_id`, `project_id`, `pledge_amt` -->
                <!-- submitted to pledge_options.py, and refreshes the page -->
                <a @click="addPledgeOption()" class="btn btn-primary">Submit</a>
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
            <a v-if="is_creator" @click="removeOption(option.price_id)" class="btn btn-danger">Remove
              option</a>
            <a v-else @click="checkoutPledge(option.price_id, option.pledge_amt)" class="btn btn-success">Pledge ${{
              option.pledge_amt}}</a>
          </div>
        </div>
      </div>
    </div>
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
      project_id: this.$route.params.project_id,
      project: {},

      product_id: '',
      options: [],
      user_id: JSON.parse(sessionStorage.getItem('user')).user_id,
      is_creator: JSON.parse(sessionStorage.getItem('user')).is_creator,
      customer_id: JSON.parse(sessionStorage.getItem('user')).customer_id,

      title: '',
      description: '',
      pledge_amt: 0,
    }
  },
  methods: {
    getDetails() {
      const url = "http://localhost:5000/project/" + this.project_id
      // const url = "http://project:5000/project/" + this.project_id
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
      // const url = "http://pledge_options:5009/options/" + this.project_id
      axios.get(url)
        .then(response => {
          this.options = response.data.data
        })
        .catch(error => {
          console.log(error.message)
        })
    },



    addPledgeOption() {
      // data submitted to pledge_options.py
      // `title`, `description`, `user_id`, `project_id`, `pledge_amt`
      const json = {
        "title": this.title,
        "description": this.description,
        "user_id": this.user_id,
        "project_id": this.project_id,
        "product_id": this.product_id,
        "pledge_amt": this.pledge_amt
      }
      const url = "http://localhost:5009/options/" + this.project_id + "/add"
      // const url = "http://pledge_options:5009/options/" + this.$route.params.project_id + "/add"
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
      // const url = "http://pledge_options:5009/options/" + price_id
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
    },


    checkoutPledge(price_id, pledge_amt) {
      // first post to back_project.py to create checkout session
      const url = "http://localhost:5004/create_checkout_session"
      // const url = "http://back_project:5004/create_checkout_session"
      const json = {
        "project_id": this.project_id,
        "pledge_amt": pledge_amt,
        "price_id": price_id,
        "quantity": 1,
        "cancel_url": "http://localhost:5173/project/" + this.project.project_id,
        "customer_id": this.customer_id
      }
      axios.post(url, json)
        .then(response => {
          console.log(response.data)
          const data = response.data
          const checkout_url = data.url
          // redirect to checkout_url for backer to key in card details
          window.location.href = checkout_url
        })
        .catch(error => {
          console.log(error.message)
        })
    },

    // cancelPledge(tracker_id) {
    //   // first post to back_project.py to create checkout session
    //   const url = "http://localhost:5004/create_checkout_session"
    //   // const url = "http://back_project:5004/create_checkout_session"
    //   const json = {
    //     "project_id": this.project_id,
    //     "pledge_amt": pledge_amt,
    //     "price_id": price_id,
    //     "quantity": 1,
    //     "cancel_url": "http://localhost:5173/project/" + this.project.project_id,
    //     "customer_id": this.customer_id
    //   }
    //   axios.post(url, json)
    //     .then(response => {
    //       console.log(response.data)
    //       const data = response.data
    //       const checkout_url = data.url
    //       // redirect to checkout_url for backer to key in card details
    //       window.location.href = checkout_url
    //     })
    //     .catch(error => {
    //       console.log(error.message)
    //     })
    // },


  
  },
  mounted() {
    this.getDetails()
    this.getOptions()
    // this.isCreator()

  },
}
</script>