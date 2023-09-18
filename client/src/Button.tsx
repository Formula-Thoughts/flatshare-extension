import React, { MouseEventHandler } from "react";
import styled from "styled-components";

const Wrapper = styled.a`
  background-color: white;
  color: #322848;
  padding: 20px;
  border-radius: 10px;
  font-size: 25px;
  border: 0;
  cursor: pointer;

  &::-moz-focus-inner,
  &::-moz-focus-inner {
    border: 0;
    padding: 0;
  }
`;

type Props = {
  onClick?: MouseEventHandler<HTMLAnchorElement> | undefined;
  children?: React.ReactNode;
  style?: React.CSSProperties | undefined;
};

const Button = (props: Props) => {
  return (
    <Wrapper onClick={props.onClick} style={props.style} className="secondary">
      {props.children}
    </Wrapper>
  );
};

export default Button;
