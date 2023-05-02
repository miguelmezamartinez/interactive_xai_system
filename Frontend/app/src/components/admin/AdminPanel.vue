<template>
  <div class="bg-white shadow-md px-8 py-4 text-left">
    <h2 class="font-bold text-xl">List of Experiments</h2>
    <h4 class="pb-4">Click on an experiment to see details</h4>
    <ul>
      <li
        class="text-primary-light font-bold mb-1 cursor-pointer"
        @click="showExistingOverlay = experiment"
        v-for="experiment in experimentList"
        :key="experiment"
      >
        {{ experiment }}
      </li>
    </ul>
    <default-button
      class="mt-6"
      :color="'positive'"
      :hoverColor="'positive-dark'"
      @click="showNewOverlay = true"
      >Create new experiment</default-button
    >
    <existing-experiment-overlay
      v-if="showExistingOverlay"
      @close="closeOverlay"
      :experimentName="showExistingOverlay"
    ></existing-experiment-overlay>
    <new-experiment-overlay v-if="showNewOverlay" @close="closeOverlay">
    </new-experiment-overlay>
  </div>
</template>

<script>
import ExistingExperimentOverlay from "./ExistingExperimentOverlay.vue";
import NewExperimentOverlay from "./NewExperimentOverlay.vue";
import DefaultButton from "../buttons/DefaultButton.vue";
  /**
   * Component for the admin panel.
   */
export default {
  components: {
    DefaultButton,
    ExistingExperimentOverlay,
    NewExperimentOverlay,
  },
  mounted() {
    this.sendExperimentRequest();
  },
  data() {
    return {
      /**
       * Array of all existing experiments
       */
      experimentList: [],
      /**
       * Name of an existing experiment for which the overlay is shown.
       * If empty, no overlay is displayed.
       */
      showExistingOverlay: "",
      /**
       * Determines if the New Experiment Overlay is shown.
       */
      showNewOverlay: false,
    };
  },
  methods: {
    /**
     * Triggered when an overlay emits the 'close' event.
     * This method closes the overlay.
     */
    closeOverlay() {
      this.showExistingOverlay = "";
      this.showNewOverlay = false;
      this.sendExperimentRequest();
    },
    /**
     * Sends a request to the api to get the existing experiments
     */
    sendExperimentRequest() {
      const axios = require("axios");
      axios.get(this.apiUrl + "experiment/all").then((response) => {
        this.experimentList = response.data;
      });
    },
  },
  inject: ["apiUrl"],
};
</script>

<style>
</style>