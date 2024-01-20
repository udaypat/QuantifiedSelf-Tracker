<template>
  <div class="body text-center">
    <main class="form-signup">
      <form @submit.prevent="createUser" method="post">
        <h1 class="h3 mb-3 fw-normal">Please sign up</h1>

        <div class="form-floating">
          <input
            type="username"
            name="user"
            class="form-control"
            id="floatingInput"
            placeholder="username"
            v-model="userdata.username"
            required
          />
          <label for="floatingInput">Username</label>
        </div>

        <div class="form-floating">
          <input
            type="email"
            name="email"
            class="form-control"
            id="floatingInput"
            placeholder="email"
            v-model="userdata.email"
            required
          />
          <label for="floatingInput">Email</label>
        </div>

        <div class="form-floating">
          <input
            type="password"
            name="passwd"
            class="form-control"
            id="floatingPassword"
            placeholder="Password"
            v-model="userdata.password"
            required
          />
          <label for="floatingPassword">Password</label>
        </div>

        <div>
          <button class="w-100 btn btn-lg btn-primary" type="submit">
            Sign up
          </button>
        </div>
        <br />
        <div>
          <router-link
            class="w-100 btn btn-lg btn-secondary"
            to="/"
            type="button"
            >Go back
          </router-link>
        </div>
      </form>
      <br />
      <div v-if="error && !usrCreated" class="alert alert-danger" role="alert">
        User Already Exists
      </div>
      <div v-if="usrCreated" class="alert alert-primary" role="alert">
        Username created Successfully. Click Go back
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "SignUp",
  data() {
    return {
      userdata: {
        username: "",
        email: "",
        password: "",
      },
      error: false,
      usrCreated: false,
    };
  },
  methods: {
    createUser() {
      console.log("clicked submit");
      const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.userdata),
      };

      fetch(`${process.env.VUE_APP_BACKEND_ENDPOINT}/register`, options)
        .then((response) => response.json())
        .then((response) => {
          if (response == "User already Exists") {
            console.log(response);
            this.error = true;
          } else {
            console.log("redirecting");
            this.usrCreated = true;
            // this.$router.push("/");
          }
        })
        .catch((err) => console.error(err));
    },
  },
};
</script>

<style scoped>
html,
.body {
  display: flex;
  align-items: center;
  padding-top: 170px;
  padding-bottom: 40px;
}

.form-signup {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}

.form-signup .form-floating:focus-within {
  z-index: 2;
}

.form-signup input[type="username"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signup input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
