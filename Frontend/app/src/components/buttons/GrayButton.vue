<template>
  <div>
    <button
      v-if="!this.selected"
      class="
        btn
        border border-gray-light
        hover:border-gray
        bg-gray-light
        hover:bg-gray
        px-2
        py-1
        rounded-md
      "
    >
      <!-- The button's content -->
      <slot />
    </button>
    <button
      v-else
      class="
        btn
        bg-gray-light
        hover:bg-gray
        text-primary-light
        px-2
        py-1
        rounded-md
        border border-primary-light
      "
    >
      <slot />
    </button>
  </div>
</template>

<script>
/**
 * Component for a gray button to be used in the filter and customize menus
 */
export default {
  props: {
    /**
     * Specifies if the button should be marked as selected
     */
    selected: Boolean,
  },
};
</script>