<template>
  <div>
    <div class="d-flex align-items-end justify-content-end">
      <router-link class="btn btn-info" to="/dashboard">Home</router-link>
      <router-link class="btn btn-danger" role="button" to="/"
        >Log Out</router-link
      >
    </div>
    <section class="h-100 h-custom">
      <div class="container py-5 h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col-lg-8 col-xl-6">
            <div class="card rounded-3">
              <div class="card-body p-4 p-md-5">
                <h3 class="mb-4 pb-2 pb-md-0 mb-md-5 px-md-2">
                  Create Tracker
                </h3>

                <form
                  @submit.prevent="Createtracker"
                  class="px-md-2"
                  method="post"
                >
                  <div class="form-outline mb-4">
                    <input
                      v-model="TrackerData.name"
                      name="tname"
                      type="text"
                      class="form-control"
                      required
                    />

                    <label class="form-label">Name</label>
                  </div>
                  <div class="form-outline mb-4">
                    <input
                      v-model="TrackerData.desc"
                      name="desc"
                      type="text"
                      class="form-control"
                      required
                    />
                    <label class="form-label">Description</label>
                  </div>

                  <div class="col-md-6 mb-4">
                    <label>Type</label>
                    <select v-model="TrackerData.type" name="type" required>
                      <option value="1">Numerical</option>
                      <option value="2">Multiple Choice</option>
                      <option value="3">Duration</option>
                      <option value="4">Boolean</option>
                    </select>
                  </div>

                  <div v-if="TrackerData.type == 2" class="form-outline mb-4">
                    <input
                      v-model="TrackerData.settings"
                      name="settings"
                      type="text"
                      class="form-control"
                    />
                    <label class="form-label">Choices</label>
                  </div>
                  <button class="w-100 btn btn-lg btn-primary" type="submit">
                    Submit
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "CreateTracker",
  data() {
    return {
      TrackerData: {
        name: "",
        desc: "",
        type: "",
        settings: "",
      },
    };
  },
  methods: {
    Createtracker() {
      // console.log("clicked submit");
      // console.log(this.TrackerData);
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: localStorage.getItem("access_key"),
        },
        body: JSON.stringify(this.TrackerData),
      };
      fetch(`${process.env.VUE_APP_BACKEND_ENDPOINT}/create_tracker`, options)
        .then((response) => response.json())
        .then(() => this.$router.push("/dashboard"))
        .catch((err) => console.error(err));
    },
  },
};
</script>

<style scoped></style>
