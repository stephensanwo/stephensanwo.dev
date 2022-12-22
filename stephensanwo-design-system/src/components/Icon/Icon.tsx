import Arrow_NE from "../../assets/svg/arrow_ne.svg";
import React from "react";
import { IconInterface, IconTypes } from "./types";

const getIcon = (name: string) => {
  switch (name) {
    case IconTypes.Arrow_NE:
      return Arrow_NE;
    default:
      return null;
  }
};

const Icon: React.FC<IconInterface> = ({ type, ...props }) => {
  return <img src={`${getIcon(type)}`} alt={"icon"} width={16} height={16} />;
};

export default Icon;
