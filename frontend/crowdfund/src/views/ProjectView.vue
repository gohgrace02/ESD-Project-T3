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
      <button class="btn btn-secondary d-flex justify-content-between pe-3 ps-1" @click="back()">
        <svg width="25" height="25" viewBox="0 0 1024 1024" fill="#ffffff" class="icon" version="1.1"
          xmlns="http://www.w3.org/2000/svg">
          <path
            d="M669.6 849.6c8.8 8 22.4 7.2 30.4-1.6s7.2-22.4-1.6-30.4l-309.6-280c-8-7.2-8-17.6 0-24.8l309.6-270.4c8.8-8 9.6-21.6 2.4-30.4-8-8.8-21.6-9.6-30.4-2.4L360.8 480.8c-27.2 24-28 64-0.8 88.8l309.6 280z"
            fill="" stroke="white" stroke-width="15" />
        </svg> Back
      </button>
    </div>
    <div>
      <Logout />
    </div>
  </div>
  <div class="container-fluid">

    <!-- ######################################################################################################## -->
    <!-- ######################################################################################################## -->

    <!-- project id, name and description -->
    <div class="row">
      <p class="text-secondary mb-0">[ID: {{ project.project_id}}]</p>
      <h1>{{project.name}}</h1>
      <div class="row">
        <p>{{ project.description}}</p>
      </div>
    </div>

    <!-- ######################################################################################################## -->
    <!-- ######################################################################################################## -->

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

    <!-- ######################################################################################################## -->
    <!-- ######################################################################################################## -->

    <!-- pledge options -->
    <div class="row mb-3">
      <div class="col">
        <label for="pledge_options" class="fw-bold" style="vertical-align: middle;">Pledge options</label>
      </div>
      <div v-if="is_creator" class="col text-end">
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addPledgeOptionModal">+ Add pledge
          option</button>
      </div>
      <!-- add pledge option modal -->
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
            <p class="card-text mb-2">{{ option.description }}</p>
            <h5 v-if="is_creator" class="card-text mb-3">${{ option.pledge_amt }}</h5>
            <a v-if="is_creator" @click="removeOption(option.price_id)" class="btn btn-danger">Remove
              option</a>
            <a v-else @click="checkoutPledge(option.price_id, option.pledge_amt)" class="btn btn-success">Pledge ${{
              option.pledge_amt}}</a>
          </div>
        </div>
      </div>
    </div>

    <!-- ######################################################################################################## -->
    <!-- ######################################################################################################## -->

    <!-- feedback -->
    <div class="feedback-header">
      <label for="details" class="fw-bold mb-3">Feedback from other backers</label>
      <div v-if="(!is_creator)" class="col text-end">
        <button data-bs-toggle="modal" data-bs-target="#submitFeedbackModal" class="btn btn-secondary p-2">
          Submit feedback <span class="ms-1"><svg viewBox="0 0 24 24" width="20" fill="none"
              xmlns="http://www.w3.org/2000/svg">
              <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
              <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
              <g id="SVGRepo_iconCarrier">
                <path
                  d="M21.2799 6.40005L11.7399 15.94C10.7899 16.89 7.96987 17.33 7.33987 16.7C6.70987 16.07 7.13987 13.25 8.08987 12.3L17.6399 2.75002C17.8754 2.49308 18.1605 2.28654 18.4781 2.14284C18.7956 1.99914 19.139 1.92124 19.4875 1.9139C19.8359 1.90657 20.1823 1.96991 20.5056 2.10012C20.8289 2.23033 21.1225 2.42473 21.3686 2.67153C21.6147 2.91833 21.8083 3.21243 21.9376 3.53609C22.0669 3.85976 22.1294 4.20626 22.1211 4.55471C22.1128 4.90316 22.0339 5.24635 21.8894 5.5635C21.7448 5.88065 21.5375 6.16524 21.2799 6.40005V6.40005Z"
                  stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                <path
                  d="M11 4H6C4.93913 4 3.92178 4.42142 3.17163 5.17157C2.42149 5.92172 2 6.93913 2 8V18C2 19.0609 2.42149 20.0783 3.17163 20.8284C3.92178 21.5786 4.93913 22 6 22H17C19.21 22 20 20.2 20 18V13"
                  stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
              </g>
            </svg></span>
        </button>
      </div>
    </div>
    <div class="row mb-3 mx-1" id="feedback">
      <div v-for="feedback in feedback_list" class="card  mb-4">
        <div class="card-body text-start">
          <h5 class="card-title">{{ feedback.name }} <span class="ms-3 fw-light">({{ feedback.rating }} ⭐️)</span></h5>
          <blockquote class="card-text mb-2 blockquote">{{ feedback.feedback_info }}</blockquote>
        </div>
      </div>
    </div>

    <!-- submit feedback modal -->
    <div class="modal fade" id="submitFeedbackModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="title">Submit feedback</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <!-- feedback form -->
          <form>
            <div class="modal-body">
              <div class="row justify-content-center my-3">
                <div class="col mx-3">
                  <div class="mb-3">
                    <label for="rating" class="form-label">Rating:</label>
                    <!-- <h5><span class="rate"><i @click="stars(1)">★</i><i @click="stars(2)">★</i><i @click="stars(3)">★</i><i
                          @click="stars(4)">★</i><i @click="stars(5)">★</i>
                    </span></h5> -->
                    <span class="rate">
                      <i v-for="index in 5" :key="index" @click="stars(index)"
                        :class="{ 'highlighted': index <= rating }">★</i>
                    </span>
                  </div>
                  <div class="mb-3">
                    <label for="description" class="form-label">Description:</label>
                    <textarea required v-model="feedback_text" class="form-control" id="feedback_text"
                      style="min-height: 120px;" placeholder="" />
                    <p class="text-danger my-3">{{ errorMsg }}</p>
                  </div>

                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <!-- things submitted: `title`, `description`, `user_id`, `project_id`, `pledge_amt` -->
              <!-- submitted to pledge_options.py, and refreshes the page -->
              <a @click="check()" class="btn btn-primary">Submit</a>
            </div>
          </form>
        </div>
      </div>
    </div>






  </div>
</template>

<script>
import axios from 'axios'
import Logout from '@/components/Logout.vue'

export default {
  components: {
    Logout
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

      feedback_list: [],
      rating: 0,
      feedback_text: '',
      errorMsg: '',
    }
  },
  methods: {
    back() {
      if (this.is_creator) {
        this.$router.push({ path: `/creator`, replace: true })
      } else {
        this.$router.push({ path: `/backer`, replace: true })
      }
    },



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
        "customer_id": this.customer_id,
        "goal_reached": this.project.goal_reached
      }
      axios.post(url, json)
        .then(response => {
          // console.log(response.data)
          const data = response.data
          const checkout_url = data.url
          // // redirect to checkout_url for backer to key in card details
          window.location.href = checkout_url
        })
        .catch(error => {
          console.log(error.message)
        })
    },


    getFeedback(){
      const url = "http://localhost:5007/get_feedback/" + this.project_id
      axios.get(url)
        .then(response => {
          this.feedback_list = response.data.feedback_list
        })
        .catch(error => {
          console.log(error.message)
        })
    },


    stars(n) {
      this.rating = n
    },


    submitFeedback() {
      const url = "http://localhost:5007/create_feedback/" + this.project_id
      const json = {
        "user_id": this.user_id,
        "rating": this.rating,
        "feedback_info": this.feedback_text
      }
      axios.post(url, json)
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.log(error.message)
        })
        .finally(() => {
          this.$router.push({ path: `/creator`, replace: true })
        })
    },


    check() {
      this.errorMsg = ''
      const json = {
        "text": this.feedback_text
      }
      axios.post("http://localhost:5006/moderate", json)
        .then(response => {
          if (response.data == '0') {
            // console.log("yes")
            this.submitFeedback()
          } else {
            this.errorMsg = 'NO F*CKING VULGARITIES ALLOWED'
          }
        })
        .catch(error => {
          console.log(error.message)
        })
    }
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
    this.getFeedback()
    // this.isCreator()

  },
}
</script>

<style>
.feedback-header {
  display: grid;
  grid-template-columns: auto 180px;
  margin-bottom: 1.5rem;
  margin-top: 0.5rem;
}

/* new */
/* .rate i {
  cursor: pointer;
  font-style: normal;
  font-size: 50px;
} */
.rate i,
.rate i:hover~i {
  color: #2222;
  text-shadow: none;
  transition: color 200ms,
    text-shadow 200ms;
  /* This will remove the delay when
     moving the cursor left or right
     within the set of stars. */
  transition-delay: 0;
  font-size: 50px;
}

/* This is the style that will be
   applied to all stars and then
   subsequently removed from the stars
   to the right of the one being
   hovered. */
.rate:hover i {
  color: #fc0;
  text-shadow: #fc0 0 0 20px;
}

/* Make the effect apply one star at a
   time. Limiting the selector to when
   .rate is hovered removes the effect
   without delay when cursor leaves
   the .rate area. */
.rate:hover i:nth-child(2) {
  transition-delay: 30ms;
}

.rate:hover i:nth-child(3) {
  transition-delay: 60ms;
}

.rate:hover i:nth-child(4) {
  transition-delay: 90ms;
}

.rate:hover i:nth-child(5) {
  transition-delay: 120ms;
}

/* Miscellaneous styles. */
.rate i {
  cursor: pointer;
  font-style: normal;
}

/* clicked */
.rate .highlighted,
.rate .highlighted:hover~.highlighted {
  color: #fc0;
  text-shadow: #fc0 0 0 20px;
}

.rate .highlighted {
  transition: color 200ms, text-shadow 200ms;
  transition-delay: 0;
}

.rate .highlighted:nth-child(2) {
  transition-delay: 30ms;
}

.rate .highlighted:nth-child(3) {
  transition-delay: 60ms;
}

.rate .highlighted:nth-child(4) {
  transition-delay: 90ms;
}

.rate .highlighted:nth-child(5) {
  transition-delay: 120ms;
}
</style>