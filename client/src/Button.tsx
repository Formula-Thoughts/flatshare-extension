import React, { MouseEventHandler } from "react";
import styled from "styled-components";

const Wrapper = styled.a<{ $disabled?: boolean }>`
  background-color: white;
  color: ${(props) => (props.$disabled ? "grey" : "#322848")};
  padding: 20px;
  border-radius: 10px;
  font-size: 20px;
  width: 200px;
  border: 0;
  cursor: ${(props) => (props.$disabled ? "not-allowed" : "pointer")};
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
  $disabled?: boolean;
};

const Button = (props: Props) => {
  return (
    <Wrapper
      $disabled={props.$disabled}
      onClick={props.$disabled ? undefined : props.onClick}
      style={props.style}
      className="secondary"
    >
      {props.children}
    </Wrapper>
  );
};

export default Button;
