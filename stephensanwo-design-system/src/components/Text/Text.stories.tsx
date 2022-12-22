import { ComponentStory, ComponentMeta } from "@storybook/react";
import Text from "./Text";

export default {
  title: "Components/Text",
  component: Text,
  argTypes: {},
} as ComponentMeta<typeof Text>;

const Template: ComponentStory<typeof Text> = (args) => <Text {...args} />;

export const Heading1 = Template.bind({});
Heading1.args = {
  type: "h1",
  children: "The quick brown fox jumps over the lazy dog",
};

export const Heading2 = Template.bind({});
Heading2.args = {
  type: "h2",
  children: "The quick brown fox jumps over the lazy dog",
};

export const Heading4 = Template.bind({});
Heading4.args = {
  type: "h4",
  children: "The quick brown fox jumps over the lazy dog",
};

export const Heading5 = Template.bind({});
Heading5.args = {
  type: "h5",
  children: "The quick brown fox jumps over the lazy dog",
};
export const Heading6 = Template.bind({});
Heading6.args = {
  type: "h6",
  children: "The quick brown fox jumps over the lazy dog",
};

export const Paragraph = Template.bind({});
Paragraph.args = {
  type: "p",
  children: "The quick brown fox jumps over the lazy dog",
};

export const Small = Template.bind({});
Small.args = {
  type: "small",
  children: "The quick brown fox jumps over the lazy dog",
};
export const ALink = Template.bind({});
ALink.args = {
  type: "a",
  children: "The quick brown fox jumps over the lazy dog",
};
