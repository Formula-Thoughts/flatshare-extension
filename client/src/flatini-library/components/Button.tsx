import React from "react";
import styled from "styled-components";
import { device } from "../util/mediaQueries";

const Primary = styled.button`
  background: ${(props) => props.theme.colors.text};
  color: ${(props) => props.theme.colors.background};
  padding: 1.5rem;
  border-radius: 0.7rem;
  font-weight: bold;
  font-size: ${(props) => props.theme.fonts.types.paragraph.size};

  &:hover {
    background: ${(props) => props.theme.colors.primary};
  }

  @media ${device.tablet} {
    padding: 1.1rem;
  }
`;

interface ButtonProps {
  label: string;
  onClick?: () => void;
  style?: React.CSSProperties;
  type?: "button" | "reset" | "submit" | undefined;
  id?: string;
  name?: string;
}

const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  style,
  type,
  id,
  name,
}) => {
  return (
    <Primary
      id={id}
      style={style}
      onClick={onClick}
      type={type ?? undefined}
      name={name}
    >
      {label}
    </Primary>
  );
};

export default Button;
