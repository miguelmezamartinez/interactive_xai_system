<template>
  <div>
    <div class="flex space-x-4 mb-4 -mt-4 self-start">
      <navigation-button :type="'dataset'"></navigation-button>
    </div>
    <login-screen
      v-if="!authenticated"
      @logged-in="authenticated = true"
    ></login-screen>
    <admin-view v-if="authenticated"></admin-view>
  </div>
</template>

<script>
import LoginScreen from "../components/admin/LoginScreen.vue";
import NavigationButton from "../components/buttons/NavigationButton.vue";
import AdminView from "../components/admin/AdminPanel.vue";

/**
 * Page for the Admin Panel. Wraps the admin panel itself, the navigation button and a login screen.
 */
export default {
  data() {
    return {
      /**
       * True if user is logged in, false otherwise
       */
      authenticated: false,
    };
  },
  components: {
    AdminView,
    LoginScreen,
    NavigationButton,
  },
};
</script>

<style>
</style>