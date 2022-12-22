import React from "react";
import Icon from "../Icon";
import { IconTypes } from "../Icon/types";
import Text from "../Text";
import "./style.css";

interface LinkButtonInterface {
  kind: "primary" | "secondary" | "tertiaty" | "danger";
  href?: string;
  text: string;
  hasIcon: boolean;
  icon?: React.ReactNode;
}

const LinkButton: React.FC<LinkButtonInterface> = ({
  kind,
  href,
  text,
  hasIcon,
  icon,
  ...rest
}) => {
  return (
    <a
      className={`button button-${kind}`}
      href={href}
      target="_blank"
      rel="noopener noreferrer"
    >
      <h6>{text}</h6>
      {hasIcon && <Icon type={IconTypes.Arrow_NE} />}
    </a>
  );
};

export default LinkButton;
