<template>
  <div>
    <div class="absolute inset-0 z-40 opacity-25 bg-black"></div>
    <div class="
        opacity-100
        fixed
        overflow-y-auto
        inset-0
        flex
        justify-center
        items-center
        z-50
      ">
      <div class="relative mx-auto w-auto">
        <div class="bg-white w-100 rounded-lg shadow-md p-4">
          <div class="flex justify-between mb-8">
            <h4 class="text-xl font-bold">Create new experiment</h4>
            <button @click="this.$emit('close')" class="bg-white hover:bg-gray-light px-2 py-0.5 rounded-full">
              <fa-icon icon="times"></fa-icon>
            </button>
          </div>
          <div class="
              grid grid-cols-auto grid-flow-col
              gap-x-8 gap-y-2
              auto-cols-max auto-rows-auto
            ">
            <div class="col-start-1 col-span-2 font-bold pt-2">
              Experiment name
            </div>
            <input class="col-start-3 col-span-3 rounded p-2" :class="getBorderStyling('name')" v-model="name"
              placeholder="Name for the experiment" />
            <div class="col-start-1"></div>
            <div class="col-start-3 text-sm text-negative mb-2">
              {{ errorMessages.name }}
            </div>
            <div class="col-start-1 col-span-2 font-bold row-span-2 pt-2">
              Description
            </div>
            <textarea placeholder="Describe your experiment" v-model="description"
              :class="getBorderStyling('description')"
              class="col-start-3 col-span-3 row-span-2 rounded resize-none p-2"></textarea>
            <div class="col-start-1"></div>
            <div class="col-start-3 text-sm text-negative mb-2">
              {{ errorMessages.description }}
            </div>
            <div class="col-start-1 col-span-2 font-bold pt-2">
              Applications the user is shown
            </div>
            <textarea v-model="applications" class="col-start-3 col-span-3 rounded resize-none p-2"
              :class="getBorderStyling('applications')"
              placeholder="IDs of the applications the user is shown, separated by comma (must be between 0 and 999)"></textarea>
            <div class="col-start-1"></div>
            <div class="col-start-3 text-sm text-negative mb-2">
              {{ errorMessages.applications }}
            </div>
            <div class="col-start-1 col-span-2 font-bold">
              Allow Modification and What-if analysis
            </div>
            <div class="col-start-3 col-span-3 space-x-4">
              <span class="space-x-2">
                <input v-model="modwhatif" type="radio" id="both" name="modwhatif" value="both" />
                <label for="both">Modification and What-if</label>
              </span>
              <span class="space-x-2">
                <input type="radio" id="modonly" name="modwhatif" v-model="modwhatif" value="modonly" />
                <label for="modonly">Modification only</label>
              </span>
              <span class="space-x-2">
                <input type="radio" id="none" name="modwhatif" value="none" v-model="modwhatif" />
                <label for="none">None</label>
              </span>
            </div>
            <div class="col-start-1"></div>
            <div class="col-start-3 col-span-3 text-sm text-negative mb-2">
              {{ errorMessages.modwhatif }}
            </div>
            <div class="col-start-1 col-span-2 font-bold">Explanation type</div>
            <div class="col-start-3 col-span-3 space-x-4">
              <span class="space-x-2">
                <input type="radio" id="lime" v-model="explanation" name="explanation" value="lime" />
                <label for="lime">Lime</label>
              </span>
              <span class="space-x-2">
                <input type="radio" id="lime_orig" name="explanation" v-model="explanation" value="lime_orig" />
                <label for="lime_orig">LIME Original</label>
              </span>
              <span class="space-x-2">
                <input type="radio" id="shap" name="explanation" v-model="explanation" value="shap" />
                <label for="shap">SHAP</label>
              </span>
              <span class="space-x-2">
                <input type="radio" id="shap_orig" name="explanation" v-model="explanation" value="shap_orig" />
                <label for="shap_orig">SHAP Original</label>
              </span>
              <span class="space-x-2">
                <input type="radio" id="dice" name="explanation" v-model="explanation" value="dice" />
                <label for="dice">Dice</label>
              </span>
              <span class="space-x-2">
                <input type="radio" id="none" name="explanation" v-model="explanation" value="none" />
                <label for="none">None</label>
              </span>
            </div>
            <div class="col-start-1"></div>
            <div class="col-start-3 text-sm text-negative mb-2">
              {{ errorMessages.explanation }}
            </div>
            <div class="col-start-1 col-span-2 font-bold pt-2">
              Survey link (optional)
            </div>
            <div class="col-start-1"></div>
            <input v-model="surveyLink" class="col-start-3 col-span-3 rounded p-2"
              :class="getBorderStyling('surveyLink')" placeholder="URL to your survey" />
            <div class="col-start-3 text-sm text-negative mb-2">
              {{ errorMessages.surveyLink }}
            </div>
            <default-button :color="'positive'" :hoverColor="'positive-dark'" class="col-start-1" @click="clickCreate">
              Create
            </default-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DefaultButton from "../buttons/DefaultButton.vue";
/**
 * An overlay where the user can create a new experiment
 */
export default {
  data() {
    return {
      /**
       * The experiment name entered by the user
       */
      name: "",
      /**
       * The experiment description entered by the user
       */
      description: "",
      /**
       * String of comma-separated loan application ids entered by the user
       */
      applications: "",
      /**
       * Array with the application ids
       */
      applicationArray: [],
      /**
       * Link to a survey entered by the user
       */
      surveyLink: "",
      /**
       * Whether modification and what-if-analysis should be allowed.
       * Can be 'both', 'modonly' or 'none'
       */
      modwhatif: "both",
      /**
       * The explanation type for the experiment. Can be 'lime', 'lime_orig', 'shap', 'shap_orig' or 'dice'.
       */
      explanation: "lime",
      /**
       * An object in which errorMessages are saved for every attribute where the input contains errors.
       */
      errorMessages: {},
    };
  },
  inject: ["apiUrl"],
  components: { DefaultButton },
  methods: {
    /**
     * Triggered when the user clicks 'Create'
     * Gets a list with existing experiments from the API and calls the validateInput methods with it.
     */
    clickCreate() {
      const axios = require('axios');
      axios.get(this.apiUrl + "experiment/all").then((response) => {
        this.validateInput(response.data);
      });
    },
    /**
     * @param {String} attribute - The attribute/field for which the border styling is applied
     * @returns {String} Tailwind classes for border styling, red border if there's an error with the attribute, regular border otherwise
     */
    getBorderStyling(attribute) {
      if (this.errorMessages[attribute]) {
        return "border-2 border-negative";
      }
      return "border";
    },
    /**
     * Sends a post request to the API to create the experiment.
     * Emits the 'close' event afterwards.
     */
    createExperiment() {
      const axios = require("axios");
      let requestBody = {};
      requestBody.experiment_name = this.name;
      requestBody.description = this.description;
      requestBody.loan_ids = this.applications.split(",").map((x) => {
        return parseInt(x, 10);
      });
      if (this.surveyLink) {
        requestBody.survey_link = this.surveyLink;
      }
      requestBody.ismodify = false;
      requestBody.iswhatif = false;
      if (this.modwhatif === "both") {
        requestBody.ismodify = true;
        requestBody.iswhatif = true;
      } else if (this.modwhatif === "modonly") {
        requestBody.ismodify = true;
      }
      requestBody.exp_type = this.explanation;
      axios.post(this.apiUrl + "experiment/creation", requestBody).then(() => {
        this.$emit("close");
      });
    },
    /**
     * Validates the inputs and sets error messages if the input is invalid for a certain attribute/field.
     * If there are no errors, the createExperiment() method is called.
     * @param {Array} experimentList - List of all existing experiments
     */
    validateInput(experimentList) {
      this.errorMessages = {};

      for (const attribute of ["name", "description", "applications"]) {
        if (!this[attribute]) {
          this.errorMessages[attribute] = "Error, field can't be empty";
        }
      }
      if (this.name.length > 100) {
        this.errorMessages.name =
          "Error, name can't be longer than 100 characters";
      } else if (experimentList.includes(this.name)) {
        this.errorMessages.name =
          "Error, an experiment with this name already exists";
      }
      if (this.description.length > 500) {
        this.errorMessages.description =
          "Error, description can't be longer than 500 characters";
      }

      this.applications = this.applications.replace(/\s/g, "");
      const applicationsPattern = RegExp("^[0-9]{1,3}(,[0-9]{1,3})*$");
      if (!applicationsPattern.test(this.applications) && this.applications) {
        this.errorMessages.applications =
          "Error, invalid format of application ids";
      }
      if (
        this.modwhatif === "both" &&
        (this.explanation === "dice" || this.explanation === "none")
      ) {
        this.errorMessages.modwhatif =
          "Error, What-if analysis is not possible with this explanation type";
      }
      const urlPattern = /\b(https?:\/\/\S*\b)/g;
      if (!urlPattern.test(this.surveyLink) && this.surveyLink) {
        this.errorMessages.surveyLink = "Error, invalid url format";
      }
      if (Object.keys(this.errorMessages).length === 0) {
        this.createExperiment();
      }
    },
  },
};
</script>

<style>
</style>