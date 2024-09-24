const path = require("path");
const HTMLPlugin = require("html-webpack-plugin");
const CopyPlugin = require("copy-webpack-plugin");
const dotenv = require("dotenv");
const webpack = require("webpack");

dotenv.config();

console.log("check env", process.env.NODE_ENV);

module.exports = {
  entry: {
    index: "./src/index.tsx",
  },
  mode: process.env.NODE_ENV === "production" ? "production" : "development",
  watch: process.env.NODE_ENV === "production" ? false : true,
  devtool: "inline-source-map",
  module: {
    rules: [
      {
        test: /\.svg$/i,
        issuer: /\.[jt]sx?$/,
        use: ["@svgr/webpack"],
      },
      {
        test: /\.(png|jpg)$/,
        type: "asset",
        parser: { dataUrlCondition: { maxSize: 1000 } },
      },
      {
        test: /\.tsx?$/,
        use: [
          {
            loader: "ts-loader",
            options: {
              compilerOptions: { noEmit: false },
            },
          },
        ],
        exclude: /node_modules/,
      },
      {
        exclude: /node_modules/,
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": JSON.stringify(process.env),
    }),
    // new webpack.DefinePlugin({
    //   "process.env.NODE_ENV": JSON.stringify(
    //     process.env.NODE_ENV || "development"
    //   ),
    // }),
    // new webpack.DefinePlugin({
    //   "process.env.NODE_ENV": JSON.stringify(
    //     process.env.NODE_ENV || "development"
    //   ),
    // }),
    new CopyPlugin({
      patterns: [
        { from: "manifest.json", to: "../manifest.json" },
        { from: "content.js", to: "../content.js" },
        { from: "background.js", to: "../background.js" },
        { from: "icons", to: "../icons" },
      ],
    }),
    ...getHtmlPlugins(["index"]),
  ],
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
  output: {
    path: path.join(__dirname, "dist/js"),
    filename: "[name].js",
  },
};

function getHtmlPlugins(chunks) {
  return chunks.map(
    (chunk) =>
      new HTMLPlugin({
        title: "React extension",
        filename: `${chunk}.html`,
        chunks: [chunk],
      })
  );
}
