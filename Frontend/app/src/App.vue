<template>
  <router-view class="m-8" />
</template>

<script>
/**
 * Main component for the whole application.
 */
export default {
  data() {
    return {
      /**
       * The api url used everywhere else in the project
       */
      apiUrl: "http://localhost:8000/",
      /**
       * Object with all attributes in their categories
       */
      attributeCategories: {
        financial: [],
        personal: [],
        loan: [],
        prediction: [],
      },
      /**
       * Object with all attributes in their categories, excluding the prediction category
       */
      reducedCategories: {
        financial: [],
        personal: [],
        loan: [],
      },
      /**
       * Obejct with general attribute data
       */
      attributeData: {
        descriptions: {},
        labels: {
          amount: "Amount",
          history: "History",
          purpose: "Purpose",
          savings: "Savings",
          available_income: "Available Income",
          residence: "Residence",
          assets: "Assets",
          other_loans: "Other Loans",
          housing: "Housing",
          previous_loans: "Previous Loans",
          job: "Job",
          other_debtors: "Other Debtors",
          people_liable: "People liable",
          duration: "Duration",
          balance: "Balance",
          age: "Age",
          telephone: "Telephone",
          employment: "Employment",
          NN_recommendation: "AI Recommendation",
          NN_confidence: "AI Confidence",
          id: "#",
        },
        categories: {},
        types: {},
        lowerBounds: {},
        upperBounds: {},
        values: {},
      },
    };
  },
  mounted() {
    this.sendAttributeRequest();
  },
  methods: {
    /**
     * Sends API request to get the attribute information and saves it in the attributeData, attributeCategories and reducedCategories variables.
     */
    sendAttributeRequest() {
      const axios = require("axios");
      axios.get(this.apiUrl + "attributes/information").then((response) => {
        for (const element of response.data) {
          this.attributeData.descriptions[element.attribute] =
            element.description;
          this.attributeData.categories[element.attribute] = element.category;
          this.attributeData.types[element.attribute] = element.type;
          this.attributeData.lowerBounds[element.attribute] =
            element.lower_bound;
          this.attributeData.upperBounds[element.attribute] =
            element.upper_bound;
          this.attributeData.values[element.attribute] = element.values;
        }
        for (const attr of Object.keys(this.attributeData.categories)) {
          if (this.attributeCategories[this.attributeData.categories[attr]]) {
            this.attributeCategories[this.attributeData.categories[attr]].push(
              attr
            );
          }
          if (this.reducedCategories[this.attributeData.categories[attr]]) {
            this.reducedCategories[this.attributeData.categories[attr]].push(
              attr
            );
          }
        }
        //Modification
        //Sort attributes alphabetically to show them in the info-card

        for (var category in this.reducedCategories) {
          let sortable = [];
          for (var att in this.reducedCategories[category]) {
            sortable.push(this.reducedCategories[category][att]);
          }

          sortable.sort();
          this.reducedCategories[category] = [];

          for (att of sortable) {
            this.reducedCategories[category].push(att);
          }
        }
      });
    },
  },
  provide() {
    return {
      attributeData: this.attributeData,
      attributeCategories: this.attributeCategories,
      apiUrl: this.apiUrl,
      reducedCategories: this.reducedCategories,
    };
  },
};
</script>

<style lang="scss">
@import url("https://cdn.jsdelivr.net/npm/plusplusjakartasans@latest/plusjakartasans.css");

#app {
  font-family: "Plus Jakarta Sans", Helvetica, Arial sans-serif;
  word-spacing: 0.08rem;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>