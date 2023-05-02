<template>
  <div class="flex space-x-2 items-center cursor-pointer bg-white shadow py-2 px-4"
    @click="this.$router.push(this.type == 'dataset' ? '/dataset' : '/admin')">
    <fa-icon size="1x" :icon="type == 'dataset' ? 'table' : 'cog'"></fa-icon>
    <div>{{ type == "dataset" ? "Dataset Explorer" : "Admin Panel" }}</div>
  </div>
</template>

<script>
/**
 * Component for a navigation button that links to the Dataset Explorer or the Admin Panel
 */
export default {
  props: {
    /**
     * The button's type, can be 'dataset' or 'admin', depending on which page it should link to
     */
    type: String,
  },
};
</script>