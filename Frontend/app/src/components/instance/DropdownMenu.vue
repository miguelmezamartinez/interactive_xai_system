<template>
  <div v-click-outside="cancel" class="shadow-blurred bg-white px-4 py-2">
    <div class="m-2 font-bold">Original value:</div>
    <div class="m-2 cursor-pointer" @click="applyValue(originalValue)">
      {{ originalValue }}
    </div>
    <hr />
    <div v-if="attributeData.types[attribute] == 'categorical'">
      <div
        class="ml-6 mr-2 my-2 cursor-pointer"
        v-for="value in attributeData.values[attribute]"
        @click="applyValue(value)"
        :key="value"
      >
        <fa-icon
          class="-ml-6 mt-0.5 absolute"
          :class="getValueStyling(value)"
          icon="check"
          v-if="selectedValue == value"
        /><span :class="getValueStyling(value)">{{ value }}</span>
      </div>
    </div>
    <div v-if="attributeData.types[attribute] == 'continuous'">
      <slider
        class="mt-12"
        :min="attributeData.lowerBounds[attribute]"
        :max="attributeData.upperBounds[attribute]"
        v-model="sliderValue"
      ></slider>
      <div class="flex mt-4 mb-1">
        <default-button
          @click="applyValue(sliderValue)"
          class="mr-4"
          :size="'sm'"
          >Apply</default-button
        >
        <clear-button :size="'sm'" @click="this.$emit('cancel')"
          >Cancel</clear-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import Slider from "@vueform/slider";
import vClickOutside from "click-outside-vue3";
import DefaultButton from "@/components/buttons/DefaultButton";
import ClearButton from "../buttons/ClearButton.vue";

/**
 * Component for the dropdown menu used to modify attribute values
 */
export default {
  directives: {
    clickOutside: vClickOutside.directive,
  },
  data() {
    return {
      /**
       * The value the slider is currently at for continuous attributes
       */
      sliderValue: this.selectedValue,
    };
  },
  components: {
    DefaultButton,
    Slider,
    ClearButton,
  },
  props: {
    /**
     * The value of the attribute in the original instance
     */
    originalValue: String,
    /**
     * The current value of the attribute
     */
    selectedValue: String,
    /**
     * The attribute name
     */
    attribute: String,
  },
  inject: ["attributeData"],
  methods: {
    /**
     * Called when the user clicks cancel.
     * Emits the 'apply-value' event with the original value
     */
    cancel() {
      this.$emit("apply-value", this.originalValue);
    },
    /**
     * Returns classes for the value styling depending on if it's modified
     * @param {String} attribute - The attribute name
     * @returns {String} Tailwind classes for attribute value styling
     */
    getValueStyling(attribute) {
      if (attribute == this.selectedValue && attribute != this.originalValue) {
        return "text-modified";
      }
      return "";
    },
    /**
     * Called when the user clicks apply.
     * Applies the newly selected value.
     */
    applyValue(value) {
      this.$emit("apply-value", value);
    },
  },
};
</script>

<style
src="@vueform/slider/themes/default.css">
@import "../../../node_modules/@vueform/slider/themes/tailwind.scss";
</style>
