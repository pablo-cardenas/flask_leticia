const config = require("./config");
const { WebpackManifestPlugin } = require("webpack-manifest-plugin");

module.exports = {
  context: config.build.context,
  mode: "production",
  output: {
    path: config.build.assetsPath,
    filename: "[name].[contenthash].js",
    publicPath: config.build.assetsURL,
  },
  devtool: "inline-source-map",
  plugins: [new WebpackManifestPlugin()],
  module: {
    rules: [
      {
        test: /\.(css)$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env", "@babel/preset-react"],
          },
        },
      },
    ],
  },
};
