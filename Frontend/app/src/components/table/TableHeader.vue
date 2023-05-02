<template>
  <tr class="text-sm">
    <th
      class="py-5 px-8 font-bold"
      v-for="attribute in attributes"
      :key="attribute"
    >
      <span @click="applySorting(attribute)" class="cursor-pointer">
        <fa-icon
          class="align-text-bottom -ml-3"
          v-if="sort_by == attribute && desc == false"
          icon="sort-up"
          size="xs"
        />
        <fa-icon
          class="align-text-top -ml-3"
          v-if="sort_by == attribute && desc == true"
          icon="sort-down"
          size="xs"
        />
        {{ labels[attribute] }}</span
      ><fa-icon
        v-if="descriptions[attribute]"
        @click="hoverText = hoverText ? '' : descriptions[attribute]"
        @mouseover="hoverText = descriptions[attribute]"
        @mouseleave="hoverText = ''"
        icon="info-circle"
        class="ml-2"
      />
      <div
        v-if="hoverText == descriptions[attribute]"
        class="mt-8 absolute z-50"
      >
        <div
          class="
            p-4
            bg-white
            font-normal
            text-primary-dark
            shadow-blurred
            rounded
          "
        >
          {{ hoverText }}
        </div>
      </div>
    </th>
  </tr>
</template>

<script>
  /**
   * A component for a table header
   */
export default {
  data() {
    return {
      /**
       * The text that should be displayed when the user hovers over the info icon next to an attribute
       */
      hoverText: "",
    };
  },
  props: {
    /**
     * Object with labels for the attributes
     */
    labels: Object,
    /**
     * Object with descriptions for the attributes
     */
    descriptions: Object,
    /**
     * Array with all attributes to be displayed in the header
     */
    attributes: Array,
    /**
     * Attribute by which the data is sorted
     */
    sort_by: String,
    /**
     * true if data is sorted descending, false otherwise
     */
    desc: Boolean,
  },
  methods: {
    /**
    * Triggered when an attribute is clicked in the table header.
    * Emits 'apply-sorting' event to the parent to sort by that attribute.
    @param {String} attribute - The attribute clicked
     */
    applySorting(attribute) {
      if (!this.sort_by) {
        return;
      }
      const newSorting = {
        sort_by: attribute,
        desc: this.desc == false && this.sort_by == attribute ? true : false,
      };
      this.$emit("apply-sorting", newSorting);
    },
  },
};
</script>