<template>
  <div>
    <div class="flex space-x-4 mb-4 -mt-4">
      <navigation-button :type="'dataset'"></navigation-button>
      <navigation-button :type="'admin'"></navigation-button>
    </div>
    <instance-view :allowMod="true" :allowWhatIf="true" :expType="expType" @switch="switchExp" :allowSwitching="true"
      :instanceInfo="instanceInfo"></instance-view>
  </div>
</template>

<script>
import NavigationButton from "../components/buttons/NavigationButton.vue";
import InstanceView from "../components/instance/InstanceView.vue";
/**
 * Component for the instance/application page. Contains navigation buttons and the instance view.
 */
export default {
  mounted() {
    this.sendInstanceRequest();
  },
  data() {
    return {
      /**
       * The instance id. Provided by an url parameter
       */
      id: this.$route.params.id,
      /**
       * The instance information.
       */
      instanceInfo: {},
      /**
       * The explanation type to be shown, can be 'lime', 'lime_orig', 'shap', 'shap_orig' or 'dice'
       */
      expType: "dice",
    };
  },
  components: { InstanceView, NavigationButton },
  methods: {
    /**
     * Triggered when the user switches the explanation type
     * @param {String} expType - The new explanation type, can be 'lime', 'lime_orig', 'shap', 'shap_orig' or 'dice'
     */
    switchExp(expType) {
      this.expType = expType;
    },
    /**
     * Navigates back to the dataset explorer.
     */
    backToDataset() {
      this.$router.push("/dataset");
    },
    /**
     * Sends an API request to get the instance information.
     */
    sendInstanceRequest() {
      const axios = require("axios");
      axios.get(this.apiUrl + "instance/" + this.id).then((response) => {
        this.instanceInfo = response.data;
      });
    },
  },
  inject: ["apiUrl"],
};
</script>

<style>
</style>