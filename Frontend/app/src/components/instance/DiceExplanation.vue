<template>
  <div class="text-left px-8 py-4 shadow-md flex-col flex bg-white">
    <div class="flex justify-between">
      <div class="flex font-bold text-lg mb-4">
        Counterfactual Explanations
        <div>
          <fa-icon @click="hover = !hover" @mouseover="hover = true" @mouseleave="hover = false" icon="info-circle"
            class="ml-2" />
          <div v-if="hover" class="mt-4 text-sm absolute z-50">
            <div class="
                p-4
                max-w-2xl
                bg-white
                font-normal
                text-primary-dark
                shadow-blurred
                rounded
              ">
              {{ description }}
            </div>
          </div>
        </div>
      </div>
      <div class="text-lg">
        {{ index + 1 + " of " + counterfactuals.length }}
      </div>
    </div>
    <div class="-mx-4 space-x-4 flex justify-between items-center">
      <div :class="getArrowStyling('left')" @click="handleClick('left')">
        <fa-icon icon="arrow-left" size="2x" />
      </div>
      <div class="shadow-md overflow-x-scroll">
        <table v-if="counterfactuals.length" class="max-w-2xl table-auto text-primary text-left">
          <thead class="bg-primary text-white">
            <table-header :labels="attributeData.labels" :descriptions="attributeData.descriptions"
              :attributes="Object.keys(counterfactuals[index])" />
          </thead>
          <tbody class="divide-gray divide-y">
            <table-row :rowData="getBaseRow(counterfactuals[index])"></table-row>
            <table-row class="text-modified font-bold" :rowData="counterfactuals[index]" />
          </tbody>
        </table>
      </div>
      <div :class="getArrowStyling('right')" @click="handleClick('right')">
        <fa-icon icon="arrow-right" size="2x" />
      </div>
    </div>
    <div class="flex my-4">
      <div class="bg-primary h-6 w-6 mr-4"></div>
      Original application
    </div>
    <div class="flex">
      <div class="bg-modified h-6 w-6 mr-4"></div>
      <div class="text-modified font-bold">Counterfactual application</div>
    </div>
  </div>
</template>

<script>
import TableHeader from "../table/TableHeader.vue";
import TableRow from "../table/TableRow.vue";
/**
 * A component for displaying the DiCE explanation.
 * It shows 5 different tables with the original instance and one counterfactual each time.
 * The user can navigate through these tables with arrow buttons.
 */
export default {
  inject: ["attributeData", "apiUrl"],
  components: { TableHeader, TableRow },
  mounted() {
    this.sendDiceRequest();
  },
  props: {
    /**
     * The instance (loan application) to be used for the explanation.
     */
    instanceInfo: {
      type: Object,
      required: true,
    },
  },
  watch: {
    instanceInfo() {
      this.index = 0;
    },
  },
  methods: {
    /**
     * Handles clicks on the arrow buttons to move through the counterfactuals
     * @param {String} direction - The direction of the arrow, can be 'left' or 'right'
     */
    handleClick(direction) {
      if (
        (this.index === 0 && direction === "left") ||
        (this.index === this.counterfactuals.length - 1 && direction == "right")
      ) {
        return;
      }
      this.index += direction === "left" ? -1 : 1;
    },
    /**
     * Returns classes for the arrow's style depending on the current position in the counterfactuals.
     * Makes the button grayed out, when it's not possible to move left/right further
     * @param {String} direction - The direction of the arrow, can be 'left' or 'right'
     * @returns {String} Tailwind classes for arrow styling
     */
    getArrowStyling(direction) {
      if (
        (this.index === 0 && direction === "left") ||
        (this.index === this.counterfactuals.length - 1 && direction == "right")
      ) {
        return "p-4 flex justify-center items-center rounded-full text-gray";
      }
      return "p-4 flex justify-center items-center rounded-full hover:bg-gray-light cursor-pointer";
    },
    /**
     * Sends a request to the API to get the counterfactuals and saves them to the counterfactuals variable
     */
    sendDiceRequest() {
      const axios = require("axios");
      axios
        .get(
          this.apiUrl + "explanations/dice?instance_id=" + this.instanceInfo.id
        )
        .then((response) => {
          this.counterfactuals = response.data.counterfactuals;
        });
    },
    /**
     * Sends a request to the API to get the counterfactuals and saves them to the counterfactuals variable
     */
    getBaseRow(cfRow) {
      return Object.fromEntries(
        Object.entries(this.instanceInfo).filter(
          ([key, value]) => cfRow[key] && value
        )
      );
    },
  },
  data() {
    return {
      /**
       * An array of all counterfactual instances
       */
      counterfactuals: [],
      /**
       * The current index when moving through the counterfactual array
       */
      index: 0,
      /**
       * Description for DiCE that shows when the user hovers over the info button
       */
      description: "The goal of counterfactual explanations is to modify the values of a given loan application in such a way that the AI prediction of the modified instance leads to the opposite prediction. In the table below, you can switch between 5 counterfactuals for the loan application above. The second row shows the modified values that lead to the new prediction while the first row shows the original values for these attributes.",
      /**
       * True while the user hovers over the info button. In that case the description overlay is shown.
       */
      hover: false
    };
  },
};
</script>