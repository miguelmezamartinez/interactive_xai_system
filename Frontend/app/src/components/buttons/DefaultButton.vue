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
   * A configurable colored button component
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
        " btn rounded-md font-bold border border-transparent" +
        " bg-" +
        this.color +
        " hover:bg-" +
        this.hoverColor +
        " text-" +
        this.textColor +
        " text-" +
        this.size
      );
    },
  },
  props: {
    /**
     * The button's main color, needs to be a color defined in tailwind.config.cs
     */
    color: {
      type: String,
      required: false,
      default: "primary",
    },
    /**
     * The button's hover color, needs to be a color defined in tailwind.config.cs
     */
    hoverColor: {
      type: String,
      required: false,
      default: "primary-dark",
    },
    /**
     * The button's text color, needs to be a color defined in tailwind.config.cs
     */
    textColor: {
      type: String,
      required: false,
      default: "white",
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
