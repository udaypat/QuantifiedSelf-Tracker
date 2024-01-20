<template>
  <div>
    <div class="d-flex align-items-end justify-content-end">
      <div>
        <button class="btn btn-warning" @click="export_csv()">Export</button>
        <router-link class="btn btn-danger" role="button" to="/"
          >Log Out</router-link
        >
      </div>
    </div>
    <div id="heading" class="position-absolute top-0 start-0">
      <h1>Welcome</h1>
    </div>

    <div class="container">
      <div class="container">
        <table class="table table-borderless">
          <tr>
            <th>Tracker</th>
            <th>Last Tracked</th>
            <th>Value</th>
          </tr>
          <tr v-for="item of trackerlist" v-bind:key="item.tid">
            <!-- Tracker Name -->
            <td>
              <router-link :to="item.tid + '/details'">{{
                item.name
              }}</router-link>
            </td>

            <!-- Latest Time -->
            <td>{{ latestList[0][item.tid][0] }}</td>

            <!-- Latest Value -->
            <td>{{ latestList[0][item.tid][1] }}</td>

            <!-- Add Log -->
            <td>
              <router-link
                class="btn btn-success"
                :to="item.tid + '/create_log'"
                >Add</router-link
              >
            </td>

            <!-- Edit Log -->
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
                      :to="'/update_tracker/' + item.tid"
                      >Edit</router-link
                    >
                  </li>
                  <li>
                    <button class="dropdown-item" @click="DeleteTracker(item)">
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
    <div class="d-flex justify-content-center">
      <router-link class="btn btn-primary" to="create_tracker">
        Add Tracker</router-link
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "DashBoard",
  data() {
    return {
      trackerlist: {},
      latestList: {},
    };
  },
  methods: {
    DeleteTracker(item) {
      const options = {
        method: "DELETE",
        headers: {
          Authorization: localStorage.getItem("access_key"),
        },
      };
      let url =
        `${process.env.VUE_APP_BACKEND_ENDPOINT}/delete_tracker/` + item.tid;
      fetch(url, options)
        .then((response) => response.json())
        .then((response) => console.log(response))
        .catch((err) => console.error(err));

      // Delete item for re-rendring
      let index = this.trackerlist.indexOf(item);
      this.trackerlist.splice(index, 1);
    },

    export_csv() {
      const options = {
        method: "GET",
        headers: {
          Authorization: localStorage.getItem("access_key"),
        },
      };

      fetch(`${process.env.VUE_APP_BACKEND_ENDPOINT}/generate_export`, options)
        .then((response) => response.json())
        .then((response) => {
          check_file(response.file_id);
        })
        .catch((err) => console.error(err));

      function check_file(file_id) {
        console.log("checkingn file");
        const interval_id = setInterval(polling, 1000);
        let i = 0;
        function polling() {
          i++;
          const options = {
            method: "GET",
            headers: {
              Authorization: localStorage.getItem("access_key"),
            },
          };
          const url =
            `${process.env.VUE_APP_BACKEND_ENDPOINT}/export/` + file_id;

          const req = fetch(url, options)
            .then((res) => {
              console.log(res.status);
              if (res.status == 200 || i == 10) {
                clearInterval(interval_id);
                res
                  .blob()
                  .then((blob) => URL.createObjectURL(blob))
                  .then((href) => {
                    Object.assign(document.createElement("a"), {
                      href,
                      download: "export.csv",
                    }).click();
                  });
              }
            })
            .catch(() => clearInterval(interval_id));

          return req;
        }
      }
    },
  },
  created() {
    fetch(`${process.env.VUE_APP_BACKEND_ENDPOINT}/trackers`, {
      headers: { Authorization: localStorage.getItem("access_key") },
    })
      .then((res) => res.json())
      .then((res) => {
        this.trackerlist = res.tlist;
        this.latestList = res.latest;
      });
  },
};
</script>

<style scoped>
.table {
  margin-top: 200px;
  /* --bs-table-bg: pink !important; */
}
.btn-primary {
  background-color: #0d6efd;
}
.btn-success {
  background-color: #198754;
}
#heading {
  margin-left: 20px;
  margin-top: 40px;
}
</style>
