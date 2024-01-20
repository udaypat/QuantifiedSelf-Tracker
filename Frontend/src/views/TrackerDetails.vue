<template>
  <div>
    <div class="d-flex align-items-end justify-content-end">
      <router-link class="btn btn-info" to="/dashboard" role="button"
        >Home</router-link
      >

      <router-link class="btn btn-danger" role="button" to="/"
        >Log Out</router-link
      >
    </div>
    <div class="container">
      <div id="heading" class="position-absolute top-0 start-0">
        <h1>{{ tracker_name }} Tracker</h1>
      </div>
    </div>

    <div class="container">
      <canvas id="myChart"></canvas>
    </div>

    <br />
    <br />
    <br />

    <div class="container">
      <table class="table table-borderless">
        <tr>
          <th>On</th>
          <th>Value</th>
          <th>Note</th>
        </tr>

        <!-- {% for i in log_list %} -->
        <tr v-for="item in logList" :key="item.lid">
          <td>{{ item.timestamp }}</td>
          <td>{{ item.val }}</td>
          <td>{{ item.note }}</td>

          <td>
            <div class="dropdown">
              <button
                class="btn btn-danger dropdown-toggle"
                type="button"
                id="dropdownMenuButton1"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Actions
              </button>
              <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                <li>
                  <router-link
                    class="dropdown-item"
                    :to="'/update_log/' + item.lid"
                    >Edit</router-link
                  >
                </li>
                <li>
                  <button class="dropdown-item" @click="DeleteLog(item)">
                    Delete
                  </button>
                </li>
              </ul>
            </div>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";

export default {
  name: "TrackerDetails",
  data() {
    return {
      logList: {},
      tracker_id: "",
      tracker_type: "",
      tracker_name: "",
      values_arr: [],
      label: "",
      chart: {},
    };
  },
  methods: {
    getLogs() {
      const options = {
        method: "GET",
        headers: {
          Authorization: localStorage.getItem("access_key"),
        },
      };
      this.tracker_id = this.$route.params.tid;

      let url =
        `${process.env.VUE_APP_BACKEND_ENDPOINT}/` + this.tracker_id + "/logs";
      fetch(url, options)
        .then((response) => response.json())
        .then((response) => {
          this.logList = response;
          this.get_trackerType();
        })
        .catch((err) => console.error(err));
    },
    get_trackerType() {
      const options = {
        method: "GET",
        headers: {
          Authorization: localStorage.getItem("access_key"),
        },
      };
      let url =
        `${process.env.VUE_APP_BACKEND_ENDPOINT}/tracker/` + this.tracker_id;
      fetch(url, options)
        .then((response) => response.json())
        .then((response) => {
          this.tracker_type = response.t_type;
          this.tracker_name = response.name;
          this.generateChart();
        })
        .catch((err) => console.error(err));
    },
    DeleteLog(item) {
      // console.log(item);
      const options = {
        method: "DELETE",
        headers: {
          Authorization: localStorage.getItem("access_key"),
        },
      };
      let url =
        `${process.env.VUE_APP_BACKEND_ENDPOINT}/delete_log/` + item.lid;
      fetch(url, options)
        .then((response) => response.json())
        .then(() => {
          this.chart.destroy();
          this.generateChart();
        })
        .catch((err) => console.error(err));

      // Delete item for re-rendring
      let index = this.logList.indexOf(item);
      this.logList.splice(index, 1);
    },
    createLinechart() {
      let myChart = document.getElementById("myChart");
      // let values_arr = this.logList.map((a) => a.val);

      function dd(tt) {
        return new Date(tt);
      }
      // console.log(dd("2021-08-10T18:45:00"), "scsai");
      let time_arr = this.logList
        .map((a) => dd(a.timestamp).toLocaleString())
        .reverse();
      // console.log(this.logList);
      // console.log(time_arr);
      // console.log(values_arr, "in line chart");
      this.chart = new Chart(myChart, {
        type: "line",
        data: {
          labels: time_arr,
          datasets: [
            {
              label: this.label,
              data: this.values_arr,
              borderColor: "rgb(51, 153, 255)",
            },
          ],
        },
      });
    },
    createPiechart() {
      // console.log("creating pie chart");
      let myChart = document.getElementById("myChart");

      // let values_arr = this.logList.map((a) => a.val);
      const counts = {};

      for (const num of this.values_arr) {
        counts[num] = counts[num] ? counts[num] + 1 : 1;
      }

      // console.log(counts);

      this.chart = new Chart(myChart, {
        type: "doughnut",
        data: {
          labels: Object.keys(counts),
          datasets: [
            {
              data: Object.values(counts),
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(102, 255, 51)",
                "rgb(255, 80, 80)",
                "rgb(54, 162, 235)",
                "rgb(254, 205, 86)",
                "rgb(51, 153, 245)",
                "rgb(102, 0, 255)",
              ],
            },
          ],
        },
      });
    },

    generateChart() {
      // console.log(this.logList);
      if (this.tracker_type == 1) {
        //Numerical
        this.values_arr = this.logList.map((a) => a.val).reverse();
        this.label = "Value";
        this.createLinechart();
      } else if (this.tracker_type == 2) {
        //Multiple
        this.values_arr = this.logList.map((a) => a.val).reverse();
        // console.log(this.values_arr);
        // console.log("multiple");
        this.createPiechart();
      } else if (this.tracker_type == 3) {
        //Duration
        this.values_arr = this.logList
          .map((a) => this.HourstoMinute(a.val))
          .reverse();
        this.label = "Duartion in Minutes";
        this.createLinechart();
      } else if (this.tracker_type == 4) {
        //Boolean
        this.values_arr = this.logList.map((a) => a.val).reverse();
        // console.log(this.values_arr);
        this.createPiechart();
        // console.log("boolean");
      }
    },
    HourstoMinute(str) {
      let [hours, minutes] = str.split(":");
      return +hours * 60 + +minutes;
    },
  },
  mounted() {
    this.getLogs();
  },
};
</script>

<style scoped>
#heading {
  margin-left: 20px;
  margin-top: 10px;
}

#myChart {
  margin-top: 30px;
  max-height: 500px;
}
</style>
