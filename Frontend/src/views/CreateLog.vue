<template>
  <div>
    <div id="heading" class="position-absolute top-0 start-0">
      <!-- <h1>{{tname}} - Tracker</h1> -->
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
                <h3 class="mb-4 pb-2 pb-md-0 mb-md-5 px-md-2">Add Log</h3>

                <form @submit.prevent="Createlog" class="px-md-2" method="post">
                  <div class="form-outline mb-4">
                    <label class="form-label">When</label>
                    <input
                      name="time"
                      type="datetime-local"
                      class="form-control"
                      v-model="Logdata.timestamp"
                    />
                  </div>

                  <label class="form-label">Value</label>

                  <!-- Numerical -->
                  <div v-if="TrackerData.t_type == 1" class="form-outline mb-4">
                    <input
                      name="value"
                      type="number"
                      step="any"
                      class="form-control"
                      v-model="Logdata.value"
                      min="0"
                      required
                    />
                  </div>

                  <!-- Multiple Choice   -->
                  <div
                    v-else-if="TrackerData.t_type == 2"
                    class="col-md-6 mb-4"
                  >
                    <select v-model="Logdata.value" name="value">
                      <option v-for="item in t_settings" :key="item">
                        {{ item }}
                      </option>
                    </select>
                  </div>

                  <!-- Duration -->
                  <div
                    v-else-if="TrackerData.t_type == 3"
                    class="col-md-6 mb-4"
                  >
                    <input v-model="Logdata.value" type="time" name="value" />
                  </div>

                  <!-- Boolean -->
                  <div
                    v-else-if="TrackerData.t_type == 4"
                    class="col-md-6 mb-4"
                  >
                    <select v-model="Logdata.value" name="value">
                      <option>True</option>
                      <option>False</option>
                    </select>
                  </div>

                  <div class="form-outline mb-4">
                    <label>Notes</label>
                    <textarea
                      v-model="Logdata.note"
                      name="notes"
                      cols="40"
                    ></textarea>
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
  name: "CreateLog",
  data() {
    return {
      TrackerData: {},
      Logdata: {
        timestamp: "",
        value: "",
        note: "",
      },
      t_settings: [],
      tracker_id: "",
    };
  },
  methods: {
    Createlog() {
      console.log("clicked submit");

      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: localStorage.getItem("access_key"),
        },
        body: JSON.stringify(this.Logdata),
      };
      let url = "http://127.0.0.1:5000/" + this.tracker_id + "/create_log";

      fetch(url, options)
        .then((response) => response.json())
        .then((response) => {
          console.log(response);
          this.$router.push("/dashboard");
        })
        .catch((err) => console.error(err));
    },
    getTracker() {
      this.tracker_id = this.$route.params.tid;
      let url = "http://127.0.0.1:5000/tracker/" + this.tracker_id;
      fetch(url, {
        method: "GET",
        headers: { Authorization: localStorage.getItem("access_key") },
      })
        .then((res) => res.json())
        .then((res) => {
          this.TrackerData = res;
          this.t_settings = res.settings.split(",");
        });
    },
  },
  beforeMount() {
    this.getTracker();
  },
};
</script>

<style scoped></style>
