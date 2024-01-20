<template>
  <div>
    <div id="heading" class="position-absolute top-0 start-0">
      <!-- <h1>{{oname}} - Tracker</h1> -->
    </div>
    <div class="d-flex align-items-end justify-content-end">
      <router-link class="btn btn-info" to="/dashboard" role="button"
        >Home</router-link
      >
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
                  Update Tracker
                </h3>
                <form class="px-md-2" @submit.prevent="updateTracker">
                  <div class="form-outline mb-4">
                    <input
                      name="tname"
                      type="text"
                      class="form-control"
                      v-model="TrackerData.name"
                      required
                    />
                    <label class="form-label">Name</label>
                  </div>

                  <div class="form-outline mb-4">
                    <input
                      name="desc"
                      type="text"
                      class="form-control"
                      v-model="TrackerData.desc"
                    />
                    <label class="form-label">Description</label>
                  </div>

                  <div class="col-md-6 mb-4">
                    <label>Type</label>
                    <select
                      v-model="TrackerData.t_type"
                      disabled
                      name="type"
                      id="Ttype"
                    >
                      <option value="1">Numerical</option>
                      <option value="2">Multiple Choice</option>
                      <option value="3">Duration</option>
                      <option value="4">Boolean</option>
                    </select>
                  </div>

                  <div v-if="TrackerData.t_type == 2" class="form-outline mb-4">
                    <input
                      name="settings"
                      type="text"
                      class="form-control"
                      v-model="TrackerData.settings"
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
  data() {
    return {
      TrackerData: {},
    };
  },
  methods: {
    getTracker() {
      let url =
        `${process.env.VUE_APP_BACKEND_ENDPOINT}/tracker/` +
        this.$route.params.tid;
      fetch(url, {
        method: "GET",
        headers: { Authorization: localStorage.getItem("access_key") },
      })
        .then((res) => res.json())
        .then((res) => {
          this.TrackerData = res;
        });
    },
    updateTracker() {
      console.log("clicked sumbit");
      const options = {
        method: "PUT",
        headers: {
          Authorization: localStorage.getItem("access_key"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.TrackerData),
      };

      fetch(
        `${process.env.VUE_APP_BACKEND_ENDPOINT}/update_tracker/${this.$route.params.tid}`,
        options
      )
        .then((response) => response.json())
        .then(() => this.$router.push("/dashboard"))
        .catch((err) => console.error(err));
    },
  },
  created() {
    this.getTracker();
  },
};
</script>

<style scoped>
#heading {
  margin-left: 20px;
  margin-top: 10px;
}
</style>
