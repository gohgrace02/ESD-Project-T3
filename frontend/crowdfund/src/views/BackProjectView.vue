<script setup>

</script>

<template>
  <div class="container-fluid">
    <form action="">
      <!-- Pledge amount -->
      <div class="row justify-content-center">
        <div class="col-md-6 col-sm-8 bg-success rounded-3 p-3">
          <div class="mb-3">
            <label for="pledge_amt" class="form-label text-light">Pledge amount:</label>
            <input type="number" class="form-control" id="pledge_amt">
          </div>
        </div>
      </div>
      <!-- Card details form -->
      <div class="row justify-content-center my-3">
        <div class="col-md-6 col-sm-8 bg-light rounded-3 p-3">
          <h1>Payment details</h1>
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input type="email" class="form-control" id="email" aria-describedby="emailHelp">
          </div>
          <div class="mb-3">
            <label for="card_number" class="form-label">Card number</label>
            <input type="text" class="form-control" id="card_number" placeholder="1234 1234 1234 1234">
          </div>
          <div class=" row mb-3">
            <div class="col">
              <label for="expiration" class="form-label">Expiration</label>
              <input type="text" class="form-control" id="expiration" placeholder="MM / YY">
            </div>
            <div class="col">
              <label for="CVC" class="form-label">CVC</label>
              <input type="number" class="form-control" id="CVC" placeholder="CVC">
            </div>
          </div>
          <div class="mb-3">
            <label for="country" class="form-label">Country</label>
            <input type="text" class="form-control" id="country" placeholder="Country">
          </div>
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
      pledge_amt: 0,
    }
  },
  methods: {
    createCheckoutSession() {
      console.log("Checkout session created")
    },
  },
  mounted() {
    this.createCheckoutSession()
  }
}
</script>
