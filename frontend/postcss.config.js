module.exports = {
  plugins: [
    require("autoprefixer"),
    require("postcss-import"),
    require("postcss-url"),
    require("postcss-inline-svg"),
    require("postcss-preset-env")({
      stage: 1
    }),
    require("postcss-nested")
  ]
};
