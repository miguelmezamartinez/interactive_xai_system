<template>
  <div v-if="confidence < 0.75" class="text-cc-low font-bold">
    <span class="rounded-lg bg-cc-low text-white px-2 py-1 mr-2"
      >{{ Math.round(confidence * 100) }}%</span
    ><span>Low <span v-if="explicit">Confidence</span></span>
  </div>
  <div v-else-if="confidence >= 0.9" class="text-cc-high font-bold">
    <span class="rounded-lg bg-cc-high text-white px-2 py-1 mr-2"
      >{{ Math.round(confidence * 100) }}%</span
    ><span>High <span v-if="explicit">Confidence</span></span>
  </div>
  <div v-else-if="confidence >= 0.75" class="text-cc-medium font-bold">
    <span class="rounded-lg bg-cc-medium text-white px-2 py-1 mr-2"
      >{{ Math.round(confidence * 100) }}%</span
    ><span>Medium <span v-if="explicit">Confidence</span></span>
  </div>
</template>

<script>
  /**
   * Component that displays a visualization of the AI's confidence
   */
export default {
  props: {
    /**
     * The value for the confidence
     */
    confidence: Number,
    /**
     * If true, the text will be e.g. 'High Confidence' instead of 'High'
     */
    explicit: Boolean,
  },
};
</script>