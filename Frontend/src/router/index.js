import Vue from "vue";
import VueRouter from "vue-router";

import SignIn from "../views/SignIn";
import SignUp from "../views/SignUp.vue";
import DashBoard from "../views/DashBoard.vue";
import CreateTracker from "../views/CreateTracker.vue";
import EditTracker from "../views/EditTracker.vue";
import TrackerDetails from "../views/TrackerDetails.vue";
import CreateLog from "../views/CreateLog.vue";
import EditLog from "../views/EditLog.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    component: SignIn,
  },

  {
    path: "/signup",
    component: SignUp,
  },
  {
    path: "/dashboard",
    component: DashBoard,
  },
  {
    path: "/create_tracker",
    component: CreateTracker,
  },
  {
    path: "/:tid/create_log",
    component: CreateLog,
  },
  {
    path: "/:tid/details",
    component: TrackerDetails,
  },
  {
    path: "/update_log/:lid",
    component: EditLog,
  },
  {
    path: "/update_tracker/:tid",
    component: EditTracker,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
