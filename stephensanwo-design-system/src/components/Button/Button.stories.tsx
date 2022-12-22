import { ComponentStory, ComponentMeta } from "@storybook/react";
import Button from "./Button";
import { action } from "@storybook/addon-actions";

export default {
  title: "Components/Button",
  component: Button,
  argTypes: {},
} as ComponentMeta<typeof Button>;

const Template: ComponentStory<typeof Button> = (args) => (
  <Button {...args} onClick={action("clicked")}></Button>
);

export const Secondary = Template.bind({});
Secondary.args = {
  kind: "secondary",
  text: "Collaborate with me",
  to: "https://www.stephensanwo.dev",
  hasIcon: true,
};
