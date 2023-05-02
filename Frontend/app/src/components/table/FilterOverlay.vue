
<template>
  <transition name="fade">
    <div class="fixed inset-0 flex justify-center items-center z-50">
      <div class="relative mx-auto w-auto">
        <div class="bg-white w-100 rounded-lg shadow-md p-4">
          <div class="flex mb-8 justify-between">
            <h4 class="text-xl font-bold">
              Click on an attribute to add a filter
            </h4>
            <button
              @click="this.$emit('close')"
              class="bg-white hover:bg-gray-light px-2 py-0.5 rounded-full"
            >
              <fa-icon icon="times"></fa-icon>
            </button>
          </div>
          <div class="flex flex-col space-y-8 mb-8">
            <div
              class="
                font-bold
                flex
                capitalize
                justify-between
                space-x-16
                items-center
              "
              v-for="category in Object.keys(attributeCategories)"
              :key="category"
            >
              <div>
                {{ category }}
              </div>
              <div class="flex space-x-4">
                <div
                  v-for="attribute of attributeCategories[category]"
                  :key="attribute"
                >
                  <gray-button
                    @click="filterAttribute = attribute"
                    :selected="false"
                    v-if="!findFilter(attribute)"
                    >{{ attributeData.labels[attribute] }}</gray-button
                  >
                  <gray-button :selected="true" v-else>
                    <span @click="filterAttribute = attribute">
                      {{ attributeData.labels[attribute] }}
                    </span>
                    <fa-icon
                      @click="removeFilter(attribute)"
                      icon="times"
                      size="sm"
                      class="ml-2 align-center inset-x-2/4 text-primary-light"
                    ></fa-icon
                  ></gray-button>
                </div>
              </div>
            </div>
          </div>
          <div class="flex flex-row-reverse">
            <outline-button @click="removeAllFilters">Reset all</outline-button>
          </div>
        </div>
      </div>
      <filter-menu
        @apply="addFilter"
        @cancel="filterAttribute = ''"
        v-if="filterAttribute && findFilter(filterAttribute) != null"
        :currentFilter="findFilter(filterAttribute)"
        :attribute="filterAttribute"
      ></filter-menu>
      <filter-menu
        @apply="addFilter"
        @cancel="filterAttribute = ''"
        v-else-if="filterAttribute"
        :currentFilter="{}"
        :attribute="filterAttribute"
      ></filter-menu>
      <div
        v-if="filterAttribute"
        class="absolute inset-0 z-40 opacity-25 bg-black"
      ></div>
    </div>
  </transition>
</template>

<script>
import OutlineButton from "../buttons/OutlineButton.vue";
import GrayButton from "../buttons/GrayButton.vue";
import FilterMenu from "./FilterMenu.vue";
/**
 * Component for the overlay in which the user can add filters.
 */
export default {
  components: { GrayButton, FilterMenu, OutlineButton },
  props: {
    /**
     * Array with information about currently applied filters
     */
    currentFilters: Array,
  },
  data() {
    return {
      /**
       * New filters to be applied
       */
      newFilters: this.currentFilters,
      /**
       * The attribute for which the filter menu is shown, when empty no filter menu is shown
       */
      filterAttribute: "",
    };
  },
  inject: ["attributeData", "attributeCategories"],

  methods: {
    /**
     * Triggered when the user clicks 'Reset All'. Emits the update-filter event with an empty array of new filters.
     */
    removeAllFilters() {
      this.newFilters = [];
      this.$emit("update-filter", this.newFilters);
    },
    /**
     * Adds a new filter. Emits the update-filter event with an array containing the new filter in addition to existing ones.
     * @param filter - Object representing the new filter
     */
    addFilter(filter) {
      if (this.findFilter(filter.attribute)) {
        this.removeFilter(filter.attribute);
      }
      if (
        (filter.values &&
          filter.values.length &&
          filter.values.length <
            this.attributeData.values[filter.attribute].length) ||
        (filter.lower_bound != null &&
          (filter.lower_bound !=
            this.attributeData.lowerBounds[filter.attribute] ||
            filter.upper_bound !=
              this.attributeData.upperBounds[filter.attribute]))
      ) {
        this.newFilters.push(filter);
      }
      this.filterAttribute = "";
      this.$emit("update-filter", this.newFilters);
    },
    /**
     * Removes a filter.
     * @param attribute - The attribute for which the filter should be removed
     */
    removeFilter(attribute) {
      for (const i in this.newFilters) {
        if (Object.values(this.newFilters[i]).indexOf(attribute) > -1) {
          this.newFilters.splice(i, 1);
          this.$emit("update-filter", this.newFilters);
          break;
        }
      }
    },
    /**
     * Finds existing filter for a given attribute
     * @returns {Object} Existing filter for the attribute, null if there is none
     */
    findFilter(attribute) {
      for (const filter of this.currentFilters) {
        if (Object.values(filter).indexOf(attribute) > -1) {
          return filter;
        }
      }
      return null;
    },
  },
};
</script>

<style scoped>
.fade-enter-from {
  opacity: 0;
}
.fade-enter-to {
  opacity: 1;
}
.fade-enter-active {
  transition: all 1s ease;
}
.fade-leave-from {
  opacity: 1;
}
.fade-leave-to {
  opacity: 0;
}
.fade-leave-active {
  transition: all 1s ease;
}
</style>


