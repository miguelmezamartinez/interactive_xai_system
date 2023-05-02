<template>
  <div v-if="tableRows[0]" class="shadow-md inline-block">
    <table class="table-auto text-primary shadow-lg text-left block">
      <thead class="bg-primary text-white sticky top-0">
        <table-header
          @apply-sorting="applySorting"
          :labels="attributeData.labels"
          :descriptions="attributeData.descriptions"
          :sort_by="optionsData.sort_by"
          :desc="optionsData.desc"
          :attributes="Object.keys(tableRows[0])"
        />
      </thead>
      <tbody class="divide-gray divide-y top-8">
        <table-row v-for="row in tableRows" :key="row.id" :rowData="row" />
      </tbody>
    </table>
  </div>
  <div v-else-if="!tableRows[0] && optionsData.filter.length" class="mt-8">
    <div class="text-3xl font-bold py-2">Nothing to show</div>
    <div class="text-lg">Try removing filters to see more results</div>
  </div>
</template>

<script>
import TableHeader from "./TableHeader.vue";
import TableRow from "./TableRow.vue";
/**
 * A Data Table component used in the Dataset Explorer
 * Renders the table based on the props provided
 */
export default {
  inject: ["attributeData"],
  props: {
    /**
     * Array with the data for the table rows that should be displayed
     */
    tableRows: Array,
    /**
     * Object with options data like filters, sorting, etc.
     * Should be equal to the request body used for the POST /table request
     */
    optionsData: Object,
  },
  components: { TableRow, TableHeader },
  methods: {
    /**
    * Triggered when the TableHeader component emits 'apply-sorting'
    * Emits 'apply-sorting' event to the parent
    @param {Object} sorting - Contains the attribute to sort by and an indicator whether to sort descending or ascending
     */
    applySorting(sorting) {
      this.$emit("apply-sorting", sorting);
    },
  },
};
</script>