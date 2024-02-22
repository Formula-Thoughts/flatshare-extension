import React, { PropsWithChildren } from "react";
import styled from "styled-components";
import Header from "../components/Header";

const Wrapper = styled.div`
  position: fixed;
  height: 100%;
  width: 100%;
`;

const Content = styled.div`
  padding: 1rem;
  height: 100%;
  background: #171113;
`;

type Props = {
  children: React.ReactNode;
};

const MainLayout = (props: Props) => {
  return (
    <Wrapper>
      <Header />
      <Content>{props.children}</Content>
    </Wrapper>
  );
};

export default MainLayout;
