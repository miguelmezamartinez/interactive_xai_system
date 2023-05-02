<template>
  <tr
    class="bg-white hover:bg-gray cursor-pointer text-sm"
    @click="
      this.$router.push({
        name: 'Application View',
        params: { id: rowData.id },
      })
    "
  >
    <td v-if="rowData.id || rowData.id === 0" class="py-5 px-8 text-primary">
      {{ rowData.id }}
    </td>
    <td
      class="py-5 px-8"
      v-for="attrName in filteredAttributes"
      :key="attrName"
    >
      {{ rowData[attrName] }}
    </td>
    <td class="py-5 px-7">
      <recommendation-vis :recommendation="rowData.NN_recommendation" />
    </td>
    <td v-if="rowData.NN_confidence" class="py-5 px-7">
      <confidence-vis :confidence="rowData.NN_confidence" />
    </td>
  </tr>
</template>

<script>
import RecommendationVis from "../ui/RecommendationVis.vue";
import ConfidenceVis from "../ui/ConfidenceVis.vue";
/**
 * Component for a single table row
 */
export default {
  components: { RecommendationVis, ConfidenceVis },
  computed: {
    /**
     * Filters the attributes to exclude the special attributes id, NN_recommendation and NN_confidence
     * @returns {Array} The filtered attributes
     */
    filteredAttributes() {
      const attributeArray = Object.keys(this.rowData);
      return attributeArray.filter((el) => {
        return !(
          el == "id" ||
          el == "NN_recommendation" ||
          el == "NN_confidence"
        );
      });
    },
  },
  props: {
    /**
     * Object with the attributes and values to be displayed in this table row.
     */
    rowData: {
      type: Object,
      required: true,
    },
  },
};
</script>