<template>
  <div
    v-click-outside="cancel"
    class="
      absolute
      mt-4
      shadow-md
      opacity-100
      z-50
      shadow-md
      bg-white
      px-6
      py-4
      text-left
      rounded-md
    "
  >
    <h4 class="mb-4 font-bold">{{ attributeData.labels[attribute] }}</h4>
    <div class="" v-if="attributeData.types[attribute] == 'categorical'">
      <div
        class=""
        v-for="value in attributeData.values[attribute]"
        :key="value"
      >
        <input
          type="checkbox"
          :id="value"
          :value="value"
          v-model="selectedValues"
        />
        <label class="capitalize ml-2" :for="value">{{ value }}</label>
      </div>
    </div>
    <div v-else-if="attribute == 'NN_confidence'">
      <slider
        class="mx-2 mt-16 mb-4"
        :step="-1"
        :format="
          function (value) {
            return Math.round(value * 100) + '%';
          }
        "
        :min="attributeData.lowerBounds[attribute]"
        :max="attributeData.upperBounds[attribute]"
        v-model="allowedRange"
      ></slider>
    </div>
    <div v-else-if="attributeData.types[attribute] == 'continuous'">
      <slider
        class="mx-2 mt-16 mb-4"
        :min="attributeData.lowerBounds[attribute]"
        :max="attributeData.upperBounds[attribute]"
        v-model="allowedRange"
      ></slider>
    </div>
    <div class="flex space-x-4 mt-4 justify-between">
      <default-button @click="applyChanges">Apply</default-button>
      <clear-button @click="cancel">Cancel</clear-button>
    </div>
  </div>
</template>

<script>
import DefaultButton from "@/components/buttons/DefaultButton";
import ClearButton from "@/components/buttons/ClearButton";
import Slider from "@vueform/slider";
import vClickOutside from "click-outside-vue3";

/**
 * Component for the filter menu for a certain attribute.
 */
export default {
  directives: {
    clickOutside: vClickOutside.directive,
  },
  mounted() {
    this.selectedValues = this.currentFilter.values ?? [];
    this.allowedRange = this.currentFilter.lower_bound
      ? [this.currentFilter.lower_bound, this.currentFilter.upper_bound]
      : [
          this.attributeData.lowerBounds[this.attribute],
          this.attributeData.upperBounds[this.attribute],
        ];
  },
  data() {
    return {
      /**
       * The allowed range for a continuous attribute, can be modified by user through moving the slider
       */
      allowedRange: Array,
      /**
       * The attribute values that should be filtered by (for categorical attributes)
       */
      selectedValues: Array,
    };
  },
  methods: {
    /**
     * Triggered when the user clicks 'Cancel'
     * Emits the 'cancel' event
     */
    cancel() {
      this.$emit("cancel");
    },
    /**
     * Triggered when the user clicks 'Apply'
     * Emits the 'apply' event and sends the new filter object as payload
     */
    applyChanges() {
      if (this.attributeData.types[this.attribute] == "categorical") {
        this.$emit("apply", {
          attribute: this.attribute,
          values: this.selectedValues,
        });
        return;
      }
      this.$emit("apply", {
        attribute: this.attribute,
        lower_bound: this.allowedRange[0],
        upper_bound: this.allowedRange[1],
      });
    },
  },
  components: {
    DefaultButton,
    ClearButton,
    Slider,
  },
  props: {
    /**
     * Object representing the currently applied filter for this attribute.
     * Should be empty if there are no filters
     */
    currentFilter: Object,
    /**
     * The attribute for which the filter menu should be displayed
     */
    attribute: String,
  },
  inject: ["attributeData"],
};
</script>
