module.exports = {
  purge: ['./public/**/*.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      boxShadow: {
        'blurred': '0 2px 10px 3px rgb(0 0 0 / 0.1)',
        'float': '0 6px 10px rgb(0 0 0 / 0.3)' // For floating action buttons
      },
      colors: {
        'modified': '#F9A825', //Color that indicates that an item/value has been modified
        'primary': '#283252', // Primary accent color, currently blue
        'primary-light': '#6578b4',
        'primary-dark': '#050F2D', // Used for hovering over a button
        'positive': '#16a34a', // Green, used to communicate approval
        'positive-dark': '#15803d',
        'positive-light': '#ABE2AB', // Lighter version of positive, should be used in table & charts
        'negative': '#dc2626', // Red, used to communicate rejection
        'negative-dark': '#b91c1c',
        'negative-light': '#FF8888', // Lighter version of negative, should be used in table & charts
        'gray': '#DFDFDF', // Used in table header
        'gray-light': '#F2F2F2', // Used for background in table rows & chosen loan application section
        'text': '#333333', // Color for normal text & titles
        'background': '#F6F1EB',

        // Modification
        // New Color Schemes
        'positive-chart': '#1E88E5',
        'positive-chart-dark': '#1D58D5',
        'negative-chart': '#FF0D57',
        'negative-chart-dark': '#DF0854',



        // Colors for the color coding for low, medium and high
        //'cc-low': '#38bdf8',
        //'cc-medium': '#0284c7',
        //'cc-high': '#075985',
        'cc-low': '#AFABAB',
        'cc-medium': '#7F7F7F',
        'cc-high': '#3B3838',
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
