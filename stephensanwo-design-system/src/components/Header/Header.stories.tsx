import { ComponentStory, ComponentMeta } from "@storybook/react";
import Header from "./Header";

export default {
  title: "Components/Header",
  component: Header,
  argTypes: {},
} as ComponentMeta<typeof Header>;

const Template: ComponentStory<typeof Header> = (args) => <Header {...args} />;

export const BasicHeader = Template.bind({});
BasicHeader.args = {
  mainTitle: "stephensanwo.dev",
  hasProductHeader: false,
};

export const ProductHeader = Template.bind({});
ProductHeader.args = {
  mainTitle: "stephensanwo.dev",
  hasProductHeader: true,
  productTitle: "Design System",
};
