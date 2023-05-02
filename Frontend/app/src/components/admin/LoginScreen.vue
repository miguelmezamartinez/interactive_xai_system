<template>
  <div @keypress.enter="clickLogin">
    <div class="font-bold text-lg mb-4">
      Please enter the admin password to enter
    </div>
    <input
      autofocus="true"
      class="mb-4 rounded border-2 p-2"
      v-model="userInput"
      type="password"
      placeholder="Password"
    />
    <default-button @click="clickLogin">Login</default-button>
  </div>
</template>

<script>
import DefaultButton from "../buttons/DefaultButton.vue";
/**
 * A login screen component that controls access to the admin panel
 */
export default {
  components: { DefaultButton },
  inject: ["apiUrl"],
  methods: {
    /**
     * Is trigerred when the user clicks the login button.
     * Sends the password to the API to check if it's correct.
     * Shows an error message if the password is wrong or emits the 'logged-in' event if it's correct.
     */
    clickLogin() {
      const axios = require("axios");
      axios
        .get(this.apiUrl + "authenticate?pwd=" + this.userInput)
        .then(() => {
          this.$emit("logged-in");
        })
        .catch(() => {
          this.userInput = "";
          alert("Sorry, wrong password!");
        });
    },
  },
  data() {
    return {
      /**
       * The password typed into the input field by the user
       */
      userInput: "",
    };
  },
};
</script>

<style>
</style>