const withMT = require("@material-tailwind/html/utils/withMT");

module.exports = withMT({
  content: [
    "./index.html",
    "./transcript.html",
    "./static/src/js/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
});
