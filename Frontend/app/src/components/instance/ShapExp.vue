<template>
  <div>
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
 * Component for the SHAP explanation visualizes the SHAP Original explanations
 */
export default {
  props: {
    /**
     * Helps d3 identify this SHAP explanation.
     * If there are two SHAP explanations displayed at the same time, they should have different ids
     */
    id: String,
    /**
     * The Explanation type. Can be 'shap_orig'
     */
    expType: String,
    /**
     * The instance for which the explanation is shown.
     */
    instance: Object,
    /**
     * True, if what-if analysis is enabled. Will make the SHAP explanation to shrink
     */
    whatif: Boolean,
  },
  watch: {
    windowWidth() {
      this.generateShapExp();
    },
    instance() {
      d3.select("#" + this.id).html(null);
      this.isLoading = true;
      this.sendExplanationRequest();
    },
    whatif() {
      if (!this.isLoading) {
        this.generateShapExp();
      }
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
       * Explanation data for the shap exp
       */
      ExpData: {
        name: "Explanation",
        baseProb: {},
        outProb: {},
        attributes: [],
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
     * The method saves the data in the required structure and calls the generateShapExp method afterwards
     * @param result - The explanation result
     */
    saveData(result) {
      (this.ExpData = {
        name: "Explanation",
        baseProb: {},
        outProb: {},
        attributes: [],
      });

      let childElement = {};
      childElement.name = "Base Pr.";
      childElement.category = "Base Probability";
      childElement.attributeValue = "base probability from historical data";

      if (this.instance.NN_recommendation == 'Approve') {
        childElement.value = Math.abs(1 - this.baseValue);
      } else {
        childElement.value = Math.abs(this.baseValue);
      }
      this.ExpData.baseProb = childElement;

      childElement = {};
      childElement.name = "Decision Pr.";
      childElement.category = "Decision Probability";
      childElement.attributeValue = "Decision Probability";
      childElement.value = this.instance.NN_confidence;
      this.ExpData.outProb = childElement;

      for (let obj of result) {
        childElement = {};
        childElement.name = this.attributeData.labels[obj.attribute];
        childElement.category = this.attributeData.categories[obj.attribute];

        childElement.attributeValue = this.instance[obj.attribute];
        this.ExpData.attributes.push(childElement);

        if (this.instance.NN_recommendation == 'Approve') {
          childElement.value = obj.influence * -1;
        } else {
          childElement.value = obj.influence;
        }
      }
      this.generateShapExp();
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
    generateShapExp() {
      this.isLoading = true;
      d3.select("#" + this.id).html(null);
      d3.select("#tootltip" + this.id).html(null);


      const w = this.whatif
        ? (window.innerWidth - 32) * 0.45
        : (window.innerWidth - 32) * 0.94;
      const h = 500;
      //const h = 1000;
      const margin = 50;



      const data = this.ExpData.attributes.sort((a, b) => Math.abs(b.value) - Math.abs(a.value));
      const baseProb = this.ExpData.baseProb.value;
      const outProb = this.ExpData.outProb.value;


      // Convert effect values to plot values
      var decreaseValue = outProb,
        increaseValue = outProb,
        totalDecrease = 0,
        totalIncrease = 0;


      for (let att of data) {
        if (att.value < 0) {
          totalDecrease += Math.abs(att.value);
          att.plotValueLeft = decreaseValue;
          decreaseValue += Math.abs(att.value);
          att.plotValueRight = decreaseValue;
          /*           //Debug
                    console.log("decrease");
                    console.log(att.plotValueLeft);
                    console.log(att.value); */
        } else {
          totalIncrease += Math.abs(att.value);
          att.plotValueRight = increaseValue;
          increaseValue -= Math.abs(att.value);
          att.plotValueLeft = increaseValue;
          /* //Debug
          console.log("increase");
          console.log(att.plotValueLeft);
          console.log(att.value); */
        }

      }


      var colors = [];
      if (this.instance.NN_recommendation == 'Approve') {
        colors = ["#1E88E5", "#FF0D57"];
      } else {
        colors = ["#FF0D57", "#1E88E5"];
      }

      const padding = 0
      const minX = Math.min(baseProb, outProb - totalIncrease) - padding;
      const maxX = Math.max(outProb, outProb + totalDecrease) + padding;

      const tooltip = d3
        .select("#tooltip" + this.id)
        .style("font-size", "16px");

      const svg = d3
        .select("#" + this.id) //make sure there's a svg element in your html file
        .append("svg")
        .attr("width", w)
        .attr("height", h + margin * 4);

      const yScale = d3
        .scaleBand()
        .range([0, h])
        .domain(data.map(s => s.name))
        .padding(0.05);


      const xScale = d3
        .scaleLinear()
        .range([0, w])
        .domain([minX, maxX]);

      svg
        .append("g")
        .attr('transform', `translate(0, ${h + margin * 3})`)
        .call(d3.axisBottom(xScale));

      svg
        .append("g")
        .attr('transform', `translate(0, ${margin * 2})`)
        .call(d3.axisBottom(xScale));

      const barGroups = svg
        .selectAll("rect")
        .data(data)
        .enter();


      barGroups
        .append("rect")
        .attr("class", "bar")
        .attr("x", g => xScale(g.plotValueLeft))
        .attr("y", 20)
        .attr("height", yScale.bandwidth())
        .attr("width", g => xScale(g.plotValueRight) - xScale(g.plotValueLeft))
        .attr("transform", `translate(0, ${margin * 2})`)
        .attr("fill", g => g.value > 0 ? colors[0] : colors[1])
        .on("mouseenter", function (event, g) {
          tooltip
            .append("div")
            .text(g.category)
            .attr("class", "tt-category pb-1 text-left capitalize");

          tooltip
            .append("div")
            .text(
              g.name + (": " + g.attributeValue)
            )
            .attr("class", "tt-name text-left pb-2 font-bold capitalize");

          tooltip
            .append("div")
            .text(
              Math.round(Math.abs(g.value) * 10000) / 10000
            )
            .style(
              "color",
              g.value > 0 ? colors[0] : colors[1]
            )
            .attr("class", "tt-value font-bold text-left");
          tooltip
            .style("opacity", 1)
            .style("margin-top", margin * 2 + 20 + yScale.bandwidth() + "px")
            .style("margin-left", xScale(g.plotValueLeft) + "px");
        })
        .on("mouseout", function () {
          tooltip.style("opacity", 0).selectAll("div").remove();
        });

      barGroups
        .append("rect")
        .attr("class", "bar")
        .attr("x", g => xScale(g.plotValueLeft))
        .attr("y", 20)
        .attr("height", yScale.bandwidth())
        .attr("width", g => xScale(g.plotValueRight) - xScale(g.plotValueLeft))
        .attr("transform", `translate(0, ${margin * 2})`)
        .attr("stroke", "white")
        .attr("fill", "white")
        .attr("fill-opacity", 0)
        .on("mouseenter", function (event, g) {
          tooltip
            .append("div")
            .text(g.category)
            .attr("class", "tt-category pb-1 text-left capitalize");

          tooltip
            .append("div")
            .text(
              g.name + (": " + g.attributeValue)
            )
            .attr("class", "tt-name text-left pb-2 font-bold capitalize");

          tooltip
            .append("div")
            .text(
              Math.round(Math.abs(g.value) * 10000) / 10000
            )
            .style(
              "color",
              g.value > 0 ? colors[0] : colors[1]
            )
            .attr("class", "tt-value font-bold text-left");
          tooltip
            .style("opacity", 1)
            .style("margin-top", margin * 2 + 20 + yScale.bandwidth() + "px")
            .style("margin-left", xScale(g.plotValueLeft) + "px");
        })
        .on("mouseout", function () {
          tooltip.style("opacity", 0).selectAll("div").remove();
        });

      barGroups
        .append("rect")
        .attr("class", "bar")
        .attr("x", g => xScale(g.plotValueLeft))
        .attr("y", g => yScale(g.name))
        .attr("height", yScale.bandwidth())
        .attr("width", g => xScale(g.plotValueRight) - xScale(g.plotValueLeft))
        .attr("transform", `translate(0, ${margin * 3})`)
        .attr("fill", g => g.value > 0 ? colors[0] : colors[1])
        .on("mouseenter", function (event, g) {
          tooltip
            .append("div")
            .text(g.category)
            .attr("class", "tt-category pb-1 text-left capitalize");

          tooltip
            .append("div")
            .text(
              g.name + (": " + g.attributeValue)
            )
            .attr("class", "tt-name text-left pb-2 font-bold capitalize");

          tooltip
            .append("div")
            .text(
              Math.round(Math.abs(g.value) * 10000) / 10000
            )
            .style(
              "color",
              g.value > 0 ? colors[0] : colors[1]
            )
            .attr("class", "tt-value font-bold text-left");
          tooltip
            .style("opacity", 1)
            .style("margin-top", yScale(g.name) + yScale.bandwidth() + margin * 3 + "px")
            .style("margin-left", xScale(g.plotValueLeft) + "px");
        })
        .on("mouseout", function () {
          tooltip.style("opacity", 0).selectAll("div").remove();
        });

      barGroups
        .append("text")
        .attr("x", g => xScale(g.plotValueRight) - 5)
        .attr("y", g => yScale(g.name) + yScale.bandwidth() * .7)
        .attr("transform", `translate(0, ${margin * 3})`)
        .attr("text-anchor", "end")
        .text(function (g) {
          if (xScale(g.plotValueRight) - xScale(g.plotValueLeft) > 160 && g.value > 0) {
            //return g.name.charAt(0).toUpperCase() + g.name.slice(1) + " : " + Math.round(Math.abs(g.value) );
            return g.name.charAt(0).toUpperCase() + g.name.slice(1);
          }
        })
        .attr("font-size", "15px")
        .attr("font-weight", "600")
        .attr("fill", "white")
        .on("mouseenter", function (event, g) {
          tooltip
            .append("div")
            .text(g.category)
            .attr("class", "tt-category pb-1 text-left capitalize");

          tooltip
            .append("div")
            .text(
              g.name + (": " + g.attributeValue)
            )
            .attr("class", "tt-name text-left pb-2 font-bold capitalize");

          tooltip
            .append("div")
            .text(
              Math.round(Math.abs(g.value) * 10000) / 10000
            )
            .style(
              "color",
              g.value > 0 ? colors[0] : colors[1]
            )
            .attr("class", "tt-value font-bold text-left");
          tooltip
            .style("opacity", 1)
            .style("margin-top", yScale(g.name) + yScale.bandwidth() + margin * 3 + "px")
            .style("margin-left", xScale(g.plotValueLeft) + "px");
        })
        .on("mouseout", function () {
          tooltip.style("opacity", 0).selectAll("div").remove();
        });

      barGroups
        .append("text")
        .attr("x", g => xScale(g.plotValueLeft) + 5)
        .attr("y", g => yScale(g.name) + yScale.bandwidth() * .7)
        .attr("text-anchor", "start")
        .attr("transform", `translate(0, ${margin * 3})`)
        .text(function (g) {
          if (xScale(g.plotValueRight) - xScale(g.plotValueLeft) > 160 && g.value < 0) {
            //return g.name.charAt(0).toUpperCase() + g.name.slice(1) + " : " + Math.round(Math.abs(g.value) );
            return g.name.charAt(0).toUpperCase() + g.name.slice(1);
          }
        })
        .attr("font-size", "15px")
        .attr("font-weight", "600")
        .attr("fill", "white")
        .on("mouseenter", function (event, g) {
          tooltip
            .append("div")
            .text(g.category)
            .attr("class", "tt-category pb-1 text-left capitalize");

          tooltip
            .append("div")
            .text(
              g.name + (": " + g.attributeValue)
            )
            .attr("class", "tt-name text-left pb-2 font-bold capitalize");

          tooltip
            .append("div")
            .text(
              Math.round(Math.abs(g.value) * 10000) / 10000
            )
            .style(
              "color",
              g.value > 0 ? colors[0] : colors[1]
            )
            .attr("class", "tt-value font-bold text-left");
          tooltip
            .style("opacity", 1)
            .style("margin-top", yScale(g.name) + yScale.bandwidth() + margin * 3 + "px")
            .style("margin-left", xScale(g.plotValueLeft) + "px");
        })
        .on("mouseout", function () {
          tooltip.style("opacity", 0).selectAll("div").remove();
        });

      svg
        .append('text')
        .attr('class', 'label')
        .attr('x', xScale(outProb))
        .attr('y', margin)
        .attr('text-anchor', 'middle')
        .text(this.ExpData.outProb.name)
        .attr("font-size", "18px")
        .attr("font-weight", "600");

      svg
        .append('text')
        .attr('class', 'label')
        .attr('x', xScale(outProb))
        .attr('y', margin * 2 - 20)
        .attr('text-anchor', 'middle')
        .text((Math.round(this.ExpData.outProb.value * 100) / 100).toString())
        .attr("font-size", "18px")
        .attr("font-weight", "600");



      svg
        .append("rect")
        .attr("class", "bar")
        .attr("x", xScale(outProb) - 1.5)
        .attr("y", 0 + margin * 2 - 10)
        .attr("height", Math.abs(xScale(baseProb) - xScale(outProb)) > 150 ? h + margin + 20 : h - 20)
        .attr("width", + 3)
        .attr("fill", "black");

      svg
        .append('text')
        .attr('class', 'label')
        .attr('x', xScale(baseProb))
        .attr('y', Math.abs(xScale(baseProb) - xScale(outProb)) > 150 ? margin : h + margin * 2)
        .attr('text-anchor', 'middle')
        .text(this.ExpData.baseProb.name)
        .attr("font-size", "18px")
        .attr("font-weight", "600");

      svg
        .append('text')
        .attr('class', 'label')
        .attr('x', xScale(baseProb))
        .attr('y', Math.abs(xScale(baseProb) - xScale(outProb)) > 150 ? margin * 2 - 20 : h + margin * 3 - 15)
        .attr('text-anchor', 'middle')
        .text((Math.round(this.ExpData.baseProb.value * 100) / 100).toString())
        .attr("font-size", "18px")
        .attr("font-weight", "600");



      svg
        .append("rect")
        .attr("class", "bar")
        .attr("x", xScale(baseProb) - 1.5)
        .attr("y", Math.abs(xScale(baseProb) - xScale(outProb)) > 150 ? margin * 2 - 10 : h + margin * 3 - 10)
        .attr("height", 20)
        .attr("width", + 3)
        .attr("fill", "black");

      svg
        .append('text')
        .attr('class', 'label')
        .attr('x', w / 2)
        .attr('y', h + margin * 3 + 35)
        .attr('text-anchor', 'middle')
        .text('Probability')
        .attr("font-size", "18px")
        .attr("font-weight", "600");

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
