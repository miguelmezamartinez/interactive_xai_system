<template>
  <div>
    <div v-if="recommendation == 'Approve'" class="text-positive-chart font-bold">
      <fa-icon icon="check-circle" size="lg"></fa-icon
      ><span class="ml-2">Approve</span>
    </div>
    <div v-if="recommendation == 'Reject'" class="text-negative-chart font-bold">
      <fa-icon icon="times-circle" size="lg"></fa-icon
      ><span class="ml-2">Reject</span>
    </div>
  </div>
</template>

<script>
/**
 * Component that displays a visualization of the AI's recommendation
 */
export default {
  props: {
    /**
     * The AI recommendation, can be 'Approve' or 'Reject'
     */
    recommendation: String,
  },
};
</script>