import React from "react";
import styled from "styled-components";
import Logo from "../flatini-library/components/Logo";

const Wrapper = styled.div`
  position: fixed;
  height: 100%;
  width: 100%;
  overflow: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */

  &::-webkit-scrollbar {
    display: none;
  }
`;

const Content = styled.div`
  padding: 1rem;
  height: 100%;
`;

type Props = {
  children: React.ReactNode;
};

const LogoLayout = (props: Props) => {
  return (
    <Wrapper>
      <Logo style={{ width: "8rem" }} />
      <Content>{props.children}</Content>
    </Wrapper>
  );
};

export default LogoLayout;
