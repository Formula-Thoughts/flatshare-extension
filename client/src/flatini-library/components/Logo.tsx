import React, { HTMLProps } from "react";
import Image from "./Image";
import styled from "styled-components";
import LogoStandard from "../assets/flatini-logo.png";

const Wrapper = styled.div``;

interface LogoProps extends HTMLProps<HTMLImageElement> {
  style?: React.CSSProperties;
}

const Logo: React.FC<LogoProps> = ({ style }) => {
  return (
    <Wrapper>
      <Image style={style} alt="logo" src={LogoStandard} />
    </Wrapper>
  );
};

export default Logo;
