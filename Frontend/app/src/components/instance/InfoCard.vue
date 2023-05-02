<template>
  <div class="bg-white shadow-md px-8 py-4 text-left">
    <!--
    <h2 class="font-bold text-lg pb-4">Current Loan Application</h2>
    -->
    <div class="flex justify-between mb-4">
      <div class="text-lg font-bold flex">
        Current Loan Application
        <fa-icon @click="hover = !hover" @mouseover="hover = true" @mouseleave="hover = false" icon="info-circle"
          class="ml-2" />
        <div v-if="hover" class="mt-4 text-sm absolute z-50">
          <img src="../../assets/Attributes.png" alt="Attributes.png" />
        </div>
      </div>
    </div>
    <div>

    </div>
    <div class="flex text-sm justify-between">
      <div class="grid grid-cols-auto grid-flow-col gap-x-6 grid-rows-8"
        v-for="category in Object.keys(reducedCategories)" :key="category">
        <div class="col-span-2 col-start-1 text-lg capitalize -mt-2 mb-1">
          {{ category }}
        </div>
        <div class="col-start-1 text-primary-light font-bold" v-for="attribute in reducedCategories[category]"
          :key="attribute">
          {{ attributeData.labels[attribute] }}:
        </div>
        <div class="col-start-2 capitalize" v-for="attribute in reducedCategories[category]" :key="attribute">
          <span :class="getValueStyling(attribute)" @click="dropDownAction(attribute)">
            {{ modifiedInstance[attribute] }}
          </span>
          <fa-icon v-if="modificationEnabled && dropdownAttribute != attribute" class="ml-2 cursor-pointer"
            icon="caret-down" @click="dropdownAttribute = attribute" />
          <fa-icon v-if="modificationEnabled && dropdownAttribute == attribute" class="ml-2 cursor-pointer"
            icon="caret-up" @click="dropdownAttribute = ''" />
          <dropdown-menu class="absolute mt-1" v-if="attribute == dropdownAttribute"
            :originalValue="instanceInfo[attribute]" :selectedValue="modifiedInstance[attribute]" :attribute="attribute"
            @apply-value="applyValue" @cancel="dropdownAttribute = ''"></dropdown-menu>
        </div>
      </div>
      <div class="flex flex-col justify-start space-y-12">
        <div class="flex flex-col space-y-4 -mt-2">
          <div class="text-lg">
            <span v-if="
              newPrediction != null &&
              JSON.stringify(instanceInfo) != JSON.stringify(modifiedInstance)
            ">
              Original
            </span>
            AI Recommendation
          </div>
          <div class="flex space-x-4">
            <recommendation-vis class="" :recommendation="instanceInfo.NN_recommendation" />
            <confidence-vis class="" :confidence="instanceInfo.NN_confidence" :explicit="true" />
          </div>
        </div>
        <div class="flex flex-col space-y-4" v-if="
          newPrediction != null &&
          JSON.stringify(instanceInfo) != JSON.stringify(modifiedInstance)
        ">
          <div class="text-lg">New AI Recommendation</div>
          <div class="flex space-x-4">
            <recommendation-vis class="" :recommendation="newPrediction.NN_recommendation" />
            <confidence-vis class="" :confidence="newPrediction.NN_confidence" :explicit="true" />
          </div>
        </div>
      </div>
    </div>
    <div class="flex">
      <default-button class="col-start-1 mt-4" @click="modificationEnabled = true"
        v-if="modifiable && !modificationEnabled">Modify</default-button>
      <default-button class="col-start-1 mt-4 mr-4" @click="this.$emit('generate-explanation', modifiedInstance)" v-if="
        JSON.stringify(instanceInfo) != JSON.stringify(modifiedInstance) &&
        allowWhatIf
      ">Generate New Explanation</default-button>
      <clear-button class="col-start-2 mt-4" @click="resetInstance()" v-if="
        JSON.stringify(instanceInfo) != JSON.stringify(modifiedInstance) &&
        allowWhatIf
      ">Reset</clear-button>
      <outline-button class="col-start-2 mt-4" @click="resetInstance()" v-else-if="modificationEnabled">Reset
      </outline-button>
    </div>
  </div>
</template>

<script>
import DefaultButton from "../buttons/DefaultButton.vue";
import ConfidenceVis from "../ui/ConfidenceVis.vue";
import DropdownMenu from "./DropdownMenu.vue";
import RecommendationVis from "../ui/RecommendationVis.vue";
import ClearButton from "../buttons/ClearButton.vue";
import OutlineButton from "../buttons/OutlineButton.vue";

/**
 * This component displays a given instance and the AI recommendation.
 * Depending on the props it also allows modification and generating the new explanation and what-if analysis.
 */
export default {
  data() {
    return {
      /**
       * True while the user hovers over the info button. In that case the description overlay is shown.
       */
      hover: false,
      /**
       * The attribute for which a dropdown menu is displayed, if empty no menu is shown.
       */
      dropdownAttribute: "",
      /**
       * Specifies whether the user has enabled the modification
       */
      modificationEnabled: false,
      /**
       * The new AI prediction if the instance has been modified
       */
      newPrediction: null,
    };
  },
  components: {
    RecommendationVis,
    ConfidenceVis,
    DefaultButton,
    OutlineButton,
    DropdownMenu,
    ClearButton,
  },
  props: {
    /**
     * Object with the original instance (attributes as keys and corresponding values)
     */
    instanceInfo: Object,
    /**
     * Specifies if the user can modify the instance.
     */
    modifiable: Boolean,
    /**
     * Object with the user-modified instance (attributes as keys and corresponding values)
     */
    modifiedInstance: Object,
    /**
     * Specifies if the 'Generate New Explanation' button is shown and if the user can see the what-if analysis
     */
    allowWhatIf: Boolean,
    /*
       * Modification
       * New Propops
       * Add prop to reset modification functionality
      * */
    resetModificationFunction: Boolean,
  },
  methods: {
    /**
     * Sends a request to the API to get the new AI prediction if the instance has been modified
     */
    sendPredictionRequest() {
      // eslint-disable-next-line no-unused-vars
      const { id, NN_recommendation, NN_confidence, ...reducedInstance } =
        this.modifiedInstance;
      const axios = require("axios");
      axios
        .post(this.apiUrl + "instance/predict", reducedInstance)
        .then((response) => {
          this.newPrediction = response.data;
          //Modification
          // Add emit event
          this.$emit('new-prediction', this.newPrediction);
        });
    },
    /**
     * Triggered when user clicks 'Reset'
     * Resets the InfoCard and emits the 'reset-instance' event
     */
    resetInstance() {
      this.modificationEnabled = false;
      this.dropdownAttribute = "";
      this.newPrediction = null;
      this.$emit("reset-instance");
    },
    /**
     * Returns classes for the value styling depending on if it's modified
     * @param {String} attribute - The attribute name
     * @returns {String} Tailwind classes for attribute value styling
     */
    getValueStyling(attribute) {
      if (this.instanceInfo[attribute] != this.modifiedInstance[attribute]) {
        return "text-modified font-bold";
      }
      return "";
    },
    /**
     * Triggered when the dropdown menu emits the 'apply-value' event.
     * Passes on the information to the parent by emitting the 'apply-modification' event with the new modification
     * and calls the sendPredictionRequest() method.
     */
    applyValue(value) {
      const modification = { attribute: this.dropdownAttribute, value: value };
      this.dropdownAttribute = "";
      this.$emit("apply-modification", modification);
      this.sendPredictionRequest();
    },
    dropDownAction(attribute) {
      if (this.modificationEnabled == true) {
        if (this.dropdownAttribute == attribute) {
          this.dropdownAttribute = "";
        } else {
          this.dropdownAttribute = attribute;
        }

      }
    },
  },
  watch: {
    // Modification
    // Monitor change in loan application in experiment to reset the modification functionality.
    resetModificationFunction() {
      this.modificationEnabled = false;
      this.dropdownAttribute = "";
      this.newPrediction = null;
    },
  },
  inject: ["reducedCategories", "apiUrl", "attributeData"],
};
</script>

<style scoped>
.grid-rows-8 {
  grid-template-rows: repeat(8, minmax(0, 1fr));
}
</style>