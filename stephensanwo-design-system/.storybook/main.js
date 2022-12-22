module.exports = {
  stories: ["../src/**/*.stories.mdx", "../src/**/*.stories.@(js|jsx|ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    "@storybook/preset-create-react-app",
  ],

  // webpackFinal: async (config, { configType }) => {
  //   config.module.rules = config.module.rules.map((rule) => {
  //     if (rule.oneOf) {
  //       rule.oneOf = rule.oneOf.map((item) => {
  //         if (item.loader && item.loader.includes("file-loader")) {
  //           item.exclude.push(/\.inline\.svg$/);
  //         }
  //         return item;
  //       });
  //     }
  //     return rule;
  //   });
  //   config.module.rules.push({
  //     test: /\.inline\.svg$/,
  //     use: [{ loader: require.resolve("svg-inline-loader") }],
  //   });
  // },
  framework: "@storybook/react",
  core: {
    builder: "@storybook/builder-webpack5",
  },
};
