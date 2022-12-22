import { ComponentStory, ComponentMeta } from "@storybook/react";
import LinkButton from "./LinkButton";
import { action } from "@storybook/addon-actions";

export default {
  title: "Components/LinkButton",
  component: LinkButton,
  argTypes: {},
} as ComponentMeta<typeof LinkButton>;

const Template: ComponentStory<typeof LinkButton> = (args) => (
  <LinkButton {...args}></LinkButton>
);

export const Secondary = Template.bind({});
Secondary.args = {
  kind: "secondary",
  text: "Collaborate with me",
  href: "https://www.stephensanwo.dev",
  hasIcon: true,
};
