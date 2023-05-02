<template>
  <div>
    <button :class="getStyling()">
      <!-- The button's content -->
      <slot />
    </button>
  </div>
</template>

<script>
/**
 * A configurable outline button component
 */
export default {
  methods: {
    /**
     * Returns classes for the button's style depending on the props provided
     * @returns {String} Tailwind classes for button styling
     */
    getStyling() {
      let paddingClass = "";
      switch (this.size) {
        case "sm":
          paddingClass = "px-2 py-1";
          break;
        case "base":
          paddingClass = "px-4 py-2";
          break;
        case "lg":
          paddingClass = "px-4 py-2";
          break;
        default:
          paddingClass = "px-6 py-3";
      }
      return (
        paddingClass +
        " btn rounded-md bg-white font-bold border hover:bg-gray-light" +
        " text-" +
        this.color +
        " border-" +
        this.color +
        " text-" +
        this.size
      );
    },
  },
  props: {
    /**
     * The button's text and border color, needs to be a color defined in tailwind.config.cs
     */
    color: {
      type: String,
      required: false,
      default: "primary",
    },
    /**
    The button's size, can be sm, base, lg, xl, 2xl, ..., 9xl
    */
    size: {
      type: String,
      required: false,
      default: "lg",
    },
  },
};
</script>