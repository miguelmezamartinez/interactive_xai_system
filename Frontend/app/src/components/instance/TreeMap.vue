<template>
  <div>
    <!-- Modification
      Remove Baseline Probability in text form
      -->
    <!--
    <div class="flex justify-start mb-4 ml-1" v-if="expType == 'shap' && baseValue">
      <span class="font-bold mr-2">Average AI prediction: </span>
      <span class="text-positive">Approve with {{ Math.round((1 - baseValue) * 100) }} % confidence
      </span>
    </div>
    -->
    <div v-if="isLoading" class="my-4 flex items-center justify-start space-x-2">
      <svg role="status" class="mr-2 w-8 h-8 text-gray-light animate-spin" viewBox="0 0 100 101" fill="primary"
        xmlns="http://www.w3.org/2000/svg">
        <path
          d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
          fill="currentColor" />
        <path
          d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
          fill="currentFill" />
      </svg>
      <div>Loading...</div>
    </div>
    <div :id="'tooltip' + id" class="tooltip"></div>
    <div :id="id" />
  </div>
</template>

<script>
import * as d3 from "d3";

/**
 * Component for the treemap that visualizes the LIME, SHAP and SHAP Original explanations
 */
export default {
  props: {
    /**
     * Helps d3 identify this TreeMap.
     * If there are two treemaps displayed at the same time, they should have different ids
     */
    id: String,
    /**
     * The Explanation type. Can be 'lime', 'shap' or 'shap_orig'
     */
    expType: String,
    /**
     * The instance for which the explanation is shown.
     */
    instance: Object,
    /**
     * True, if what-if analysis is enabled. Will make the treemap shrink
     */
    whatif: Boolean,
    /**
     * If true the detail view is shown, if false the simple view
     */
    detailView: Boolean,
  },
  watch: {
    windowWidth() {
      this.generateTreeMap();
    },
    instance() {
      d3.select("#" + this.id).html(null);
      this.isLoading = true;
      this.sendExplanationRequest();
    },
    whatif() {
      if (!this.isLoading) {
        this.generateTreeMap();
      }
    },
    detailView() {
      this.generateTreeMap();
    },
    expType() {
      d3.select("#" + this.id).html(null);
      this.isLoading = true;
      this.sendExplanationRequest();
    },
  },
  data() {
    return {
      /**
       * The window's inner width
       */
      windowWidth: window.innerWidth,
      /**
       * The reference provided by the API to check the status of the explanation request and get the results.
       */
      href: "",
      /**
       * The base value provided by SHAP
       */
      baseValue: 0,
      /**
       * Indicates if the treemap is currently loading and controls if the loading animation is shown.
       */
      isLoading: true,
      /**
       * Explanation data for the simple view
       */
      simpleExpData: {
        name: "Explanation",
        children: [
          { name: "positive", children: [] },
          { name: "negative", children: [], },
        ],
      },
      /**
       * Explanation data for the detail view
       */
      detailExpData: {
        name: "Explanation",
        children: [
          {
            name: "positive",
            children: [
              { name: "financial", children: [] },
              { name: "personal", children: [] },
              { name: "loan", children: [] },
              { name: "baseline", children: [] },
            ],
          },
          {
            name: "negative",
            children: [
              { name: "financial", children: [] },
              { name: "personal", children: [] },
              { name: "loan", children: [] },
              { name: "baseline", children: [] },
            ],
          },
        ],
      },
    };
  },
  inject: ["attributeData", "apiUrl"],
  mounted() {
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.sendExplanationRequest();
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    /**
     * Called when the window is resized
     */
    onResize() {
      this.windowWidth = window.innerWidth;
    },
    /**
     * Called once the explanation result has been obtained from the API
     * The method saves the data in the required structure and calls the generateTreemap method afterwards
     * @param result - The explanation result
     */
    saveData(result) {
      (this.simpleExpData = {
        name: "Explanation",
        children: [
          { name: "positive", children: [] },
          { name: "negative", children: [], },
        ],
      }),
        (this.detailExpData = {
          name: "Explanation",
          children: [
            {
              name: "positive",
              children: [
                { name: "financial", children: [] },
                { name: "personal", children: [] },
                { name: "loan", children: [] },
                { name: "baseline", children: [] },
              ],
            },
            {
              name: "negative",
              children: [
                { name: "financial", children: [] },
                { name: "personal", children: [] },
                { name: "loan", children: [] },
                { name: "baseline", children: [] },
              ],
            },
          ],
        });
      for (let obj of result) {
        let childElement = {};
        childElement.name = this.attributeData.labels[obj.attribute];
        childElement.category = this.attributeData.categories[obj.attribute];
        childElement.value = Math.abs(obj.influence);
        childElement.attributeValue = this.instance[obj.attribute];

        let catObj;
        if (obj.influence < 0) {
          for (let category of this.detailExpData.children[0].children) {
            if (category.name === this.attributeData.categories[obj.attribute]) {
              catObj = category;
            }
          }
        } else {
          for (let category of this.detailExpData.children[1].children) {
            if (category.name === this.attributeData.categories[obj.attribute]) {
              catObj = category;
            }
          }
        }
        catObj.children.push(childElement);
      }
      // Modification
      // Add baseline value according to the prediction probability

      let childElement = {};
      childElement.name = "Baseline";
      childElement.category = "baseline";
      childElement.attributeValue = "baseline decision from historical data";

      if (this.instance.NN_recommendation == 'Approve') {
        childElement.value = Math.abs(1 - this.baseValue);
        this.detailExpData.children[0].children[3].children.push(childElement);
      } else {
        childElement.value = Math.abs(this.baseValue);
        this.detailExpData.children[1].children[3].children.push(childElement);
      }

      for (let direction of [0, 1]) {
        for (let category of this.detailExpData.children[direction].children) {
          let sum = 0;
          for (let attribute of category.children) {
            sum += attribute.value;
          }
          this.simpleExpData.children[direction].children.push({
            name: category.name,
            value: sum,
          });
        }
      }
      this.generateTreeMap();
    },
    /**
     * As long as the explanation result is null the method sends a request to the API to check if the result is ready
     * and then calls itself again with a timeout
     * If the result is ready, the saveData method is called
     * @param result - The explanation result, null if there is no result yet
     * @param expType - The current explanation type
     */
    getResult(result, expType) {
      if (!result && expType == this.expType) {
        d3.select("#" + this.id).html(null);
        const axios = require("axios");
        axios
          .get(
            this.apiUrl + "explanations/" + this.expType + "?uid=" + this.href
          )
          .then((response) => {
            if (response.data.values) {
              result = response.data.values;
              this.baseValue = response.data.base_value;
              this.saveData(result);
            }
          });
        setTimeout(() => this.getResult(result, expType), 1000);
      }
      return result;
    },
    /**
     * Initiates the explanation request to the API
     * Once the request is accepted by the API it calls the getResult method
     */
    sendExplanationRequest() {
      const axios = require("axios");
      axios
        .post(this.apiUrl + "explanations/" + this.expType, {
          instance: this.instance,
        })
        .then((response) => {
          this.href = response.data.href;
          this.getResult(null, this.expType);
        });
    },
    /**
     * Generates the treemap using d3 based on the explanation data.
     */
    generateTreeMap() {
      this.isLoading = true;
      d3.select("#" + this.id).html(null);
      d3.select("#tootltip" + this.id).html(null);
      // Modification
      // Force detailView to True 
      const detailView = true;
      const w = this.whatif
        ? (window.innerWidth - 32) * 0.45
        : (window.innerWidth - 32) * 0.94;
      const h = 500;
      const hierarchy = d3
        .hierarchy(detailView ? this.detailExpData : this.simpleExpData)
        .sum((d) => d.value) //sums every child values
        .sort((a, b) => b.value - a.value), // and sort them in descending order
        // Modification
        // Change Padding
        treemap = d3
          .treemap()
          .size([w, h])
          // .padding(this.detailView ? 1 : 2),
          .padding(1),
        root = treemap(hierarchy);

      // Modification
      // Change colors
      //var colors = ["#15803d", "#b91c1c"],
      var colors = ["#1E88E5", "#FF0D57"];

      var colorScale = d3
        .scaleOrdinal() // the scale function
        .domain(["positive", "negative"]) // the data
        .range(colors); // the way the data should be shown

      const tooltip = d3
        .select("#tooltip" + this.id)
        .style("font-size", "16px");

      const svg = d3
        .select("#" + this.id) //make sure there's a svg element in your html file
        .append("svg")
        .attr("width", w)
        .attr("height", h);

      svg
        .selectAll("rect")
        .data(root.leaves())
        .enter()
        .append("rect")
        .attr("x", (d) => d.x0)
        .attr("y", (d) => d.y0)
        .attr("width", (d) => d.x1 - d.x0)
        .attr("height", (d) => d.y1 - d.y0)
        .attr("fill", function (d) {
          return colorScale(
            detailView ? d.parent.parent.data.name : d.parent.data.name
          );
        })
        .attr("fill-opacity", 1.0)
        .on("mouseenter", function (event, d) {
          if (detailView) {
            tooltip
              .append("div")
              .text(d.parent.data.name)
              .attr("class", "tt-category pb-1 text-left capitalize");
          }

          tooltip
            .append("div")
            .text(
              d.data.name + (detailView ? ": " + d.data.attributeValue : "")
            )
            .attr("class", "tt-name text-left pb-2 font-bold capitalize");
          // Modification 
          // Remove negative symbol
          tooltip
            .append("div")
            .text(
              //(d.parent.data.name == "negative" || d.parent.parent.data.name == "negative" ? "-" : "") +
              Math.round(d.data.value * 10000) / 100 +
              (this.expType == "lime" ? "" : "%")
            )
            .style(
              "color",
              colorScale(
                detailView ? d.parent.parent.data.name : d.parent.data.name
              )
            )
            .attr("class", "tt-value font-bold text-left");

          tooltip
            .style("opacity", 1)
            .style("margin-top", d.y0 + 8 + "px")
            .style("margin-left", d.x0 + 8 + "px");
        })
        .on("mouseout", function () {
          tooltip.style("opacity", 0).selectAll("div").remove();
        });

      svg
        .selectAll("text")
        .data(root.leaves())
        .enter()
        .append("text")
        .attr("x", (d) => d.x0 + 10)
        .attr("y", (d) => d.y0 + 25)
        .text(function (d) {
          if (d.x1 - d.x0 >= 140 && d.y1 - d.y0 >= 50) {
            return d.data.name.charAt(0).toUpperCase() + d.data.name.slice(1);
          }
        })
        .attr("font-size", "15px")
        .attr("font-weight", "600")
        .attr("fill", "white");

      svg
        .selectAll("vals")
        .data(root.leaves())
        .enter()
        .append("text")
        .attr("x", (d) => d.x0 + 10)
        .attr("y", (d) => d.y0 + 45)
        .text(function (d) {
          if (d.x1 - d.x0 >= 140 && d.y1 - d.y0 >= 50) {
            return (
              // Modification 
              // Remove negative symbol
              //(d.parent.data.name == "negative" || d.parent.parent.data.name == "negative" ? "-" : "") +
              Math.round(d.data.value * 10000) / 100 +
              (this.expType == "lime" ? "" : "%")
            );
          }
        })
        .attr("font-size", "15px")
        .attr("margin-top", "16px")
        .attr("fill", "white");
      this.isLoading = false;
    },
  },
};
</script>

<style scoped>
.tooltip {
  position: absolute;
  opacity: 0;
  pointer-events: none;
  transition: all 0.2s ease-in-out;
  max-width: 400px;
  border-radius: 4px;
  background: #fff;
  box-shadow: 0 1px 5px rgba(51, 51, 51, 0.5);
  padding: 1rem;
}

.tt-name {
  font-size: 1.4rem;
  font-weight: 1200;
}
</style>
<style src="@vueform/toggle/themes/default.css">
</style>
