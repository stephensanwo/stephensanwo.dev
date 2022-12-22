import React from "react";
import Icon from "../Icon";
import { IconTypes } from "../Icon/types";
import Text from "../Text";
import "./style.css";

interface ButtonInterface
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  kind: "primary" | "secondary" | "tertiaty" | "danger";
  to?: string;
  text: string;
  hasIcon: boolean;
  icon?: React.ReactNode;
}

const Button: React.FC<ButtonInterface> = ({
  kind,
  to,
  text,
  hasIcon,
  icon,
  ...props
}) => {
  return (
    <button className={`button button-${kind}`} {...props}>
      <h6>{text}</h6>
      {hasIcon && <Icon type={IconTypes.Arrow_NE} />}
    </button>
  );
};

export default Button;
