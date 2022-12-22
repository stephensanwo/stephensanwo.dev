import React, { Fragment } from "react";
import "../../styles/index.css";

interface TextInterface {
  type: "h1" | "h2" | "h4" | "h5" | "h6" | "p" | "small" | "a";
  children: string;
}

const Text: React.FC<TextInterface> = ({ type, ...props }) => {
  return (
    <Fragment>
      {type === "h1" && <h1 {...props}>{props.children}</h1>}
      {type === "h2" && <h2 {...props}>{props.children}</h2>}
      {type === "h4" && <h4 {...props}>{props.children}</h4>}
      {type === "h5" && <h5 {...props}>{props.children}</h5>}
      {type === "h6" && <h6 {...props}>{props.children}</h6>}
      {type === "p" && <p {...props}>{props.children}</p>}
      {type === "small" && <small {...props}>{props.children}</small>}
      {type === "a" && <a {...props}>{props.children}</a>}
    </Fragment>
  );
};

export default Text;
